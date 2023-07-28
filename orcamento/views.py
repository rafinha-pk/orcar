from datetime import date
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from .models import Clientes
from .forms import ClienteForm
from .models import Fornecedores
from .forms import FornecedorForm
from .models import Produtos
from .forms import ProdutoForm

# ORÇAMENTOS

def orcamento_index(request):
    html = "Time is"

    return HttpResponse(html)

# CLIENTES

def cliente_index(request):
    context = {}
    if request.POST:
        context["dataset"] = Clientes.objects.all().filter(
                            Q(nome__icontains= request.POST.get('busca')) |
                            Q(contato__icontains= request.POST.get('busca'))
                            ).order_by('-pk')
    else:
        context["dataset"] = Clientes.objects.all().order_by('-pk')
        
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
                            ).order_by('-pk')
    else:
        context["dataset"] = Fornecedores.objects.all().order_by('-pk')
        
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
                            ).order_by('-pk')
    else:
        context["dataset"] = Produtos.objects.all().order_by('-pk')
        
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
            valor_final = (form.instance.valor_fornecedor * 100) / (100 - form.instance.margem)

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
