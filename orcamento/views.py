from django.shortcuts import (render, get_object_or_404, HttpResponseRedirect)
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Clientes
from .forms import ClienteForm
import datetime #just 4 test

def orcamento_index(request):
	now = datetime.datetime.now()
	html = "Time is {}".format(now)

	return HttpResponse(html)

def cliente_index(request):
	context = {}
	context["dataset"] = Clientes.objects.all().order_by('-pk')

	return render(request, "cliente_index.html", context)

def cliente_detail(request, pk):
	context = {}
	context["data"] = Clientes.objects.get(id = pk)

	return render(request, "cliente_detail.html", context)

def cliente_cadastra(request):
	context = {}

	form = ClienteForm(request.POST or None)

	if form.is_valid():
		usuario_logado = User.objects.get(pk=request.user.pk)
		form.instance.criador = usuario_logado
		data_atual = datetime.date.today()
		form.instance.data_criacao = data_atual
		form.instance.data_ultimo = data_atual
		form.save()
		return HttpResponseRedirect('/cliente')

	context["form"] = form

	return render(request, "cliente_cadastra.html", context)

def cliente_atualiza(request, pk):
	context = {}
	obj = get_object_or_404(Clientes, id = pk)

	form = ClienteForm(request.POST or None, instance = obj)

	if form.is_valid():
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