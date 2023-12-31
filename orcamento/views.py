from datetime import date
from datetime import datetime
from datetime import timedelta
import re
import locale
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from .models import Clientes
from .forms import ClienteForm
from .models import Fornecedores
from .forms import FornecedorForm
from .models import Produtos
from .forms import ProdutoForm
from .models import Orcamentos
from .forms import OrcamentoForm
from .models import FormaPagamento
from .models import StatusOrcamento
from .models import RegOrcamentos
from .forms import RegOrcamentoForm

# GLOBAIS

HOJE = date.today()
HOJE_HORA = timezone.now().strftime('%Y-%m-%dT%H:%M')

# LOGIN

def login(request):
    if request.POST:
        usuario = request.POST["usuario"]
        senha = request.POST["senha"]
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            if user.is_active:
                dj_login(request, user)
                return HttpResponseRedirect('/cliente')
            else:
                html= "usuario bloqueado!"
                return HttpResponse(html)
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

def logout(request):

    dj_logout(request)
    return HttpResponseRedirect('/')

# ORÇAMENTOS

def orcamento_index(request):
    context = {}
    DATA_MAXIMA = HOJE + timedelta(days=30)
    DATA_MINIMA = HOJE - timedelta(days=30)
    lista_status = StatusOrcamento.objects.all()
    context["lista_status"] = lista_status
    context["data_hoje"] = HOJE
    context["status_aberto"] = StatusOrcamento.objects.get(id = 1)
    context["status_enviado"] = StatusOrcamento.objects.get(id = 2)
    context["status_atrasado"] = StatusOrcamento.objects.get(id = 3)
    context["status_vendido"] = StatusOrcamento.objects.get(id = 4)
    context["status_cancelado"] = StatusOrcamento.objects.get(id = 5)

    if request.POST:
        filtro_data_inicio = request.POST.get('data_inicio')
        filtro_data_final = request.POST.get('data_final')
        filtro_status = request.POST.get('status')
        filtro_meus = request.POST.get('meus')
        context["data_maxima"] = datetime.strptime(filtro_data_final, '%Y-%m-%d')
        context["data_minima"] = datetime.strptime(filtro_data_inicio, '%Y-%m-%d')
        if(filtro_status >= "0"):
            context["status"] = StatusOrcamento.objects.get(id = filtro_status)
        context["meus"] = filtro_meus
        if(filtro_meus == "1"):
            dataset = Orcamentos.objects.filter(
                            Q(data_ultimo__lte = filtro_data_final),
                            Q(data_ultimo__gte = filtro_data_inicio),
                            Q(criador = request.user),
                            )
        else:
            dataset = Orcamentos.objects.filter(
                            Q(data_ultimo__lte = filtro_data_final),
                            Q(data_ultimo__gte = filtro_data_inicio),
                            )

        if(filtro_status == "1"):
            dataset = dataset.filter(Q(status = StatusOrcamento.objects.get(id = 1)))

        elif(filtro_status == "2"):
            dataset = dataset.filter(Q(status = StatusOrcamento.objects.get(id = 2)))

        elif(filtro_status == "3"):
            dataset = dataset.filter(Q(status = StatusOrcamento.objects.get(id = 3)))

        elif(filtro_status == "4"):
            dataset = dataset.filter(Q(status = StatusOrcamento.objects.get(id = 4)))

        elif(filtro_status == "5"):
            dataset = dataset.filter(Q(status = StatusOrcamento.objects.get(id = 5)))

        context["dataset"] = dataset.order_by('status', '-data_ultimo')
    else:
        if request.user.is_authenticated:

            # fazer uma verificação da data_ultimo < data_vencimento
            vencidos = Orcamentos.objects.filter(
                                Q(data_vencimento__lt = HOJE
                                    ), Q(criador = request.user)).exclude(
                                        status = StatusOrcamento.objects.get(id = 3)
                                        ).exclude(
                                        status = StatusOrcamento.objects.get(id = 4)
                                        ).exclude(
                                        status = StatusOrcamento.objects.get(id = 5)
                                        )
            for vencido in vencidos:
                vencido.status = StatusOrcamento.objects.get(id = 3)
                vencido.save()

            context["data_maxima"] = DATA_MAXIMA
            context["data_minima"] = DATA_MINIMA
            context["meus"] = "1"
            context["dataset"] = Orcamentos.objects.all().filter(
                                Q(data_ultimo__gte = DATA_MINIMA), 
                                Q(data_ultimo__lte = DATA_MAXIMA),
                                Q(criador = request.user)
                                ).order_by('status', '-data_ultimo')
        
    return render(request, "orcamento_index.html", context)

def orcamento_cadastra(request, pk):
    context = {}
    context["cliente"] = Clientes.objects.get(id= pk)
    VENCIMENTO = HOJE + timedelta(days=3)
    if request.POST:
        # se post
        form = OrcamentoForm(request.POST or None)
        form.instance.data_criacao = HOJE_HORA
        form.instance.data_ultimo = HOJE_HORA
        if form.is_valid():
            novo_orcamento = form.save()
            return HttpResponseRedirect('/orcamento/' + str(novo_orcamento.id))
        else:
            return render(request, 'base.html')
    else:

        form = OrcamentoForm(initial={'criador':request.user,
                                       'data_criacao': HOJE_HORA,
                                       'data_ultimo':HOJE_HORA,
                                       'data_vencimento':VENCIMENTO,
                                       'status':StatusOrcamento.objects.get(id= 1),
                                       'pagamento':FormaPagamento.objects.get(id= 1),
                                       'quantidade':0,
                                       'parcelas':1,
                                       'cliente':pk,
                                       })
        context["form"] = form
        context["hoje_hora"] = HOJE_HORA
        return render(request, "orcamento_cadastra.html", context)

def orcamento_detail(request, pk):
    context = {}
    orcamento = Orcamentos.objects.get(id= pk)
    if orcamento.criador == request.user:
        e_dono = "1"
    else:
        e_dono = "0"
    context["e_dono"] = e_dono
    if request.POST:
        novo_status = request.POST.get("status")
        novo_vencimento = request.POST.get("vencimento")
        novo_obs = request.POST.get("obs")
        if novo_obs == None:
            novo_obs = ""
        novo_status = StatusOrcamento.objects.get(id= novo_status)
        orcamento.status = novo_status
        orcamento.obs = novo_obs
        orcamento.data_ultimo = HOJE_HORA
        orcamento.data_vencimento = datetime.strptime(novo_vencimento, '%Y-%m-%d').date()
        context["log"] = orcamento.save()
    else:
        context["log"] = "não salvo"

    context["data"] = orcamento
    id_cliente = context["data"].cliente.id
    context["cliente"] = Clientes.objects.get(id= id_cliente)
    context["status_aberto"] = StatusOrcamento.objects.get(id = 1)
    context["status_enviado"] = StatusOrcamento.objects.get(id = 2)
    context["status_atrasado"] = StatusOrcamento.objects.get(id = 3)
    context["status_vendido"] = StatusOrcamento.objects.get(id = 4)
    context["status_cancelado"] = StatusOrcamento.objects.get(id = 5)
    regorcamento_obj_produtos = RegOrcamentos.objects.all().filter(orcamento= pk)
    context["regorcamentos"] = regorcamento_obj_produtos
    total_valor_fornecedor = 0
    total_valor_final = 0
    total_margem = 0
    quantidade = 0
    quantidade_item = 0
    for reg_obj_produto in regorcamento_obj_produtos:
        quantidade += reg_obj_produto.quantidade
        total_valor_fornecedor += reg_obj_produto.valor_fornecedor * reg_obj_produto.quantidade
        total_valor_final += reg_obj_produto.valor_final * reg_obj_produto.quantidade
        total_margem += reg_obj_produto.margem
        quantidade_item += 1
    if quantidade > 1:
        total_margem = total_margem / quantidade_item

    else:
        total_margem = 0
    total_margem = round(total_margem, 2)
    context["total_fornecedor"] = total_valor_fornecedor
    context["total_final"] = total_valor_final
    context["total_margem"] = total_margem
    context["quantidade"] = quantidade
    orcamento.valor_final = total_valor_final
    orcamento.valor_custo = total_valor_fornecedor
    orcamento.marge = total_margem
    orcamento.save()


    return render(request, 'orcamento_detail.html', context)

def orcamento_cadastrar_produto(request, pk):
    context = {}
    context["pk"] = pk
    if request.POST:
        context["dataset"] = Produtos.objects.all().filter(
                            Q(nome__icontains= request.POST.get('busca')) |
                            Q(pn__icontains= request.POST.get('busca'))
                            ).order_by('-pk')[:30]
    else:
        context["dataset"] = Produtos.objects.all().order_by('-pk')[:20]
        
    return render(request, "produto_index_popup.html", context)

def orcamento_cadastrar_produto_add(request, pk, produto):
    context = {}
    context["pk"] = pk
    add_produto = Produtos.objects.get(id= produto)
    context["produto"] = add_produto
    if request.POST:
        form = RegOrcamentoForm(request.POST or None)
        if form.is_valid():
            atualiza_produto = Produtos.objects.get(id= produto)
            atualiza_produto.valor_final = round(form.instance.valor_final, 2)
            atualiza_produto.valor_fornecedor = round(form.instance.valor_fornecedor, 2)
            atualiza_produto.margem = round(form.instance.margem, 2)
            atualiza_produto.fornecedor = form.instance.fornecedor
            atualiza_produto.data_ultimo = HOJE
            atualiza_produto.criador = request.user
            atualiza_orcamento = Orcamentos.objects.get(id= pk)
            atualiza_orcamento.quantidade += form.instance.quantidade
            atualiza_orcamento.data_ultimo = HOJE_HORA
            atualiza_produto.save()
            atualiza_orcamento.save()
            novo_registro= form.save()
            return HttpResponse('<script>window.close();</script>')
            
    else:
        form = RegOrcamentoForm(initial={'orcamento':pk, 
                                    'data':HOJE, 
                                    'produto': add_produto,
                                    'quantidade':'1',
                                    'fornecedor':add_produto.fornecedor,
                                    'valor_fornecedor':add_produto.valor_fornecedor,
                                    'valor_final':add_produto.valor_final,
                                    'margem':add_produto.margem,
                                    })
        context["form"] = form
        return render(request, "orcamento_registro.html", context)

def orcamento_delete_produto(request, pk, reg):
    context = {}
    orcamento = Orcamentos.objects.get(id= pk)
    registro = reg
    registro_apagar = RegOrcamentos.objects.get(id= registro)
    if request.method == "POST":
        registro_apagar.delete()
        return HttpResponse('<script>window.close();</script>')
    else:
        context["data"] = registro_apagar

    return render(request, "orcamento_registro_delete.html", context)

def orcamento_registro_produto(request, pk, reg):
    context = {}
    orcamento = Orcamentos.objects.get(id= pk)
    registro = get_object_or_404(RegOrcamentos, id=reg)
    produto = registro.produto
    context["produto"] = produto
    form = RegOrcamentoForm(request.POST or None, instance = registro)
    if request.POST:
        if form.is_valid():
            form.instance.data = HOJE 
            orcamento.data_ultimo = HOJE_HORA
            form.save()
            orcamento.save()
            produto.valor_final = form.instance.valor_final
            produto.valor_fornecedor = form.instance.valor_fornecedor
            produto.margem = form.instance.margem
            produto.fornecedor = form.instance.fornecedor
            produto.data_ultimo = HOJE
            produto.save()
            return HttpResponse('<script>window.close();</script>')
    context["form"] = form

    return render(request, "orcamento_registro.html", context)

def orcamento_imprimir(request, pk):
    context = {}
    total_registro = {}
    orcamento = Orcamentos.objects.get(id= pk)
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    orcamento.data_ultimo = orcamento.data_ultimo.strftime('%d de %B de %Y')
    context["data"] = orcamento
    id_cliente = context["data"].cliente.id
    context["cliente"] = Clientes.objects.get(id= id_cliente)
    regorcamento_obj_produtos = RegOrcamentos.objects.all().filter(orcamento= pk)
    context["regorcamentos"] = regorcamento_obj_produtos
    total_valor_fornecedor = 0
    total_valor_final = 0
    total_margem = 0
    quantidade = 0
    quantidade_item = 0
    for reg_obj_produto in regorcamento_obj_produtos:
        quantidade += reg_obj_produto.quantidade
        total_valor_fornecedor += reg_obj_produto.valor_fornecedor * reg_obj_produto.quantidade
        total_valor_final += reg_obj_produto.valor_final * reg_obj_produto.quantidade
        total_registro[reg_obj_produto.id] = reg_obj_produto.valor_final * reg_obj_produto.quantidade
        total_margem += reg_obj_produto.margem
        quantidade_item += 1
        reg_obj_produto.total = reg_obj_produto.valor_final * reg_obj_produto.quantidade
    if quantidade > 1:
        total_margem = total_margem / quantidade_item

    else:
        total_margem = 0
    total_margem = round(total_margem, 2)
    context["total_fornecedor"] = total_valor_fornecedor
    context["total_final"] = total_valor_final
    context["total_margem"] = total_margem
    context["quantidade"] = quantidade
    context["quantidade_item"] = quantidade_item
    context["total_registro"] = total_registro

    return render(request, 'orcamento_imprimir.html', context)

# CLIENTES

def cliente_index(request):
    context = {}
    if request.POST:
        context["dataset"] = Clientes.objects.all().filter(
                            Q(nome__icontains= request.POST.get('busca')) |
                            Q(contato__icontains= request.POST.get('busca'))
                            ).order_by('-pk')[:30]
    else:
        context["dataset"] = Clientes.objects.all().order_by('-pk')[:20]
        
    return render(request, "cliente_index.html", context)

def cliente_detail(request, pk):
    context = {}
    context["data"] = Clientes.objects.get(id = pk)

    return render(request, "cliente_detail.html", context)

def cliente_cadastra(request):
    context = {}
    
    if request.POST:
        form = ClienteForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cliente')
    else:
        form = ClienteForm(initial={'criador':request.user, 
                                    'data_criacao':HOJE, 
                                    'data_ultimo': HOJE
                                    })

    context["form"] = form

    return render(request, "cliente_cadastra.html", context)

def cliente_atualiza(request, pk):
    context = {}
    obj = get_object_or_404(Clientes, id=pk)
    form = ClienteForm(request.POST or None, instance = obj)
    if request.POST:
        if form.is_valid():
            #criador = models.User(pk=form.instance.criador)
            #criador = get_object_or_404(User, id=str(obj.criador))
            form.instance.data_ultimo = HOJE 
            form.save()
            return HttpResponseRedirect("/cliente/" + str(pk))
    context["form"] = form

    return render(request, "cliente_atualiza.html", context)

def cliente_delete(request, pk):
    context = {}
    obj = get_object_or_404(Clientes, id = pk)

    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/cliente/")
    else:
        context["data"] = Clientes.objects.get(id = pk)

    return render(request, "cliente_delete.html", context)

# FORNECEDORES

def fornecedor_index(request):
    context = {}
    if request.POST:
        context["dataset"] = Fornecedores.objects.all().filter(
                            Q(nome__icontains= request.POST.get('busca')) |
                            Q(contato__icontains= request.POST.get('busca'))
                            ).order_by('-pk')[:30]
    else:
        context["dataset"] = Fornecedores.objects.all().order_by('-pk')[:20]
        
    return render(request, "fornecedor_index.html", context)

def fornecedor_detail(request, pk):
    context = {}
    context["data"] = Fornecedores.objects.get(id = pk)

    return render(request, "fornecedor_detail.html", context)

def fornecedor_cadastra(request):
    context = {}
    
    if request.POST:
        form = FornecedorForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/fornecedor')
    else:
        form = FornecedorForm(initial={'criador':request.user, 
                                        'data_criacao':HOJE, 
                                        'data_ultimo': HOJE,
                                        })

    context["form"] = form

    return render(request, "fornecedor_cadastra.html", context)

def fornecedor_atualiza(request, pk):
    context = {}
    obj = get_object_or_404(Fornecedores, id=pk)
    form = FornecedorForm(request.POST or None, instance = obj)
    if request.POST:
        if form.is_valid():
            form.instance.data_ultimo = HOJE 
            form.save()
            return HttpResponseRedirect("/fornecedor/" + str(pk))
    context["form"] = form

    return render(request, "fornecedor_atualiza.html", context)

def fornecedor_delete(request, pk):
    context = {}
    obj = get_object_or_404(Fornecedores, id = pk)

    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/fornecedor/")
    else:
        context["data"] = Fornecedores.objects.get(id = pk)

    return render(request, "fornecedor_delete.html", context)

# PRODUTOS

def produto_index(request):
    context = {}
    if request.POST:
        context["dataset"] = Produtos.objects.all().filter(
                            Q(nome__icontains= request.POST.get('busca')) |
                            Q(pn__icontains= request.POST.get('busca'))
                            ).order_by('-pk')[:30]
    else:
        context["dataset"] = Produtos.objects.all().order_by('-pk')[:20]
        
    return render(request, "produto_index.html", context)

def produto_detail(request, pk):
    context = {}
    context["data"] = Produtos.objects.get(id = pk)

    return render(request, "produto_detail.html", context)

def produto_cadastra(request):
    context = {}
    
    if request.POST:
        form = ProdutoForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/produto')
    else:
        form = ProdutoForm(initial={'criador':request.user, 
                                        'data_criacao':HOJE, 
                                        'data_ultimo': HOJE,
                                        })

    context["form"] = form

    return render(request, "produto_cadastra.html", context)

def produto_atualiza(request, pk):
    context = {}
    obj = get_object_or_404(Produtos, id=pk)
    form = ProdutoForm(request.POST or None, instance = obj)
    if request.POST:
        if form.is_valid():
            form.instance.data_ultimo = HOJE 
            form.save()
            return HttpResponseRedirect("/produto/" + str(pk))
    context["form"] = form

    return render(request, "produto_atualiza.html", context)

def produto_delete(request, pk):
    context = {}
    obj = get_object_or_404(Produtos, id = pk)

    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/produto/")
    else:
        context["data"] = Produtos.objects.get(id = pk)

    return render(request, "produto_delete.html", context)
