from datetime import date
from django.shortcuts import (render, get_object_or_404, HttpResponseRedirect)
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from .models import Clientes
from .forms import ClienteForm


def orcamento_index(request):
    html = "Time is"

    return HttpResponse(html)

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
        form = ClienteForm(initial={'criador':request.user, 'data_criacao':HOJE, 'data_ultimo': HOJE})

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