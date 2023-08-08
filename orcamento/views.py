from datetime import date
from datetime import datetime
from datetime import timedelta
import re
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

# LOGIN

def login(request):
    html = "Time is"
    if request.POST:
        usuario = request.POST["usuario"]
        senha = request.POST["senha"]
        user = authenticate(request, username=usuario, password=senha)
        html = "Usuario: " + usuario + " - senha: " + senha
        if user is not None:
            if user.is_active:
                dj_login(request, user)
                return HttpResponseRedirect('/cliente')
            else:
                html= "usuario bloqueado!"
                return HttpResponse(html)
        else:
            return HttpResponse(html)
            #return HttpResponseRedirect('/fornecedor')
    else:
        return HttpResponse(html)

def logout(request):

    dj_logout(request)
    return HttpResponseRedirect('/cliente')

# ORÇAMENTOS

def orcamento_index(request):
    context = {}
    HOJE = date.today()
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

    HOJE = date.today()
    HOJE_HORA = timezone.now().strftime('%Y-%m-%dT%H:%M')
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
    context["data"] = Orcamentos.objects.get(id= pk)
    id_cliente = context["data"].cliente.id
    context["cliente"] = Clientes.objects.get(id= id_cliente)
    context["status_aberto"] = StatusOrcamento.objects.get(id = 1)
    context["status_enviado"] = StatusOrcamento.objects.get(id = 2)
    context["status_atrasado"] = StatusOrcamento.objects.get(id = 3)
    context["status_vendido"] = StatusOrcamento.objects.get(id = 4)
    context["status_cancelado"] = StatusOrcamento.objects.get(id = 5)
    context["regorcamentos"] = RegOrcamentos.objects.all().filter(orcamento= pk) 

    HOJE = date.today()
    HOJE_HORA = timezone.now().strftime('%Y-%m-%dT%H:%M')
    return render(request, 'orcamento_detail.html', context)

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
    HOJE = date.today()
    
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
            HOJE = date.today()
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
    HOJE = date.today()
    
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
            #criador = models.User(pk=form.instance.criador)
            #criador = get_object_or_404(User, id=str(obj.criador))
            HOJE = date.today()
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
    HOJE = date.today()
    
    if request.POST:
        form = ProdutoForm(request.POST or None)
        if form.is_valid():
            #valor_final = (form.instance.valor_fornecedor * (
                          #100/ form.instance.margem
                          #)) / ((
                          #100 / form.instance.margem)-1)
            
            #form.instance.valor_final = valor_final

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
        #form.instance.margem = "20,00"#round(form.instance.margem, 2)
        #form.instance.valor_fornecedor = "96,00"#round(form.instance.valor_fornecedor, 2)
        #form.instance.valor_final = "120,00"#round(form.instance.valor_final, 2)
        if form.is_valid():
            HOJE = date.today()
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
