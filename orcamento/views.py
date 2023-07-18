from django.shortcuts import render
from django.http import HttpResponse
from .models import Clientes
from .forms import ClienteForm
import datetime #just 4 test

def orcamento_index(request):
	now = datetime.datetime.now()
	html = "Time is {}".format(now)

	return HttpResponse(html)

def cliente_index(request):
	context = {}
	context["dataset"] = Clientes.objects.all()

	return render(request, "cliente_index.html", context)
