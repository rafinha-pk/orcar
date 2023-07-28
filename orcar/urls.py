"""orcar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from orcamento import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.orcamento_index),
    # path('orcamento/<int:pk>/', views.orcamento_detail),
    path('cliente/', views.cliente_index, name="cliente"),
    path('cliente/cadastrar', views.cliente_cadastra, name="cliente_cadastrar"),
    path('cliente/<int:pk>/', views.cliente_detail, name="cliente_detail"),
    path('cliente/<int:pk>/atualiza', views.cliente_atualiza, name="cliente_atualiza"),
    path('cliente/<int:pk>/delete', views.cliente_delete, name="cliente_delete"),

    path('fornecedor/', views.fornecedor_index, name="fornecedor"),
    path('fornecedor/cadastrar', views.fornecedor_cadastra, name="fornecedor_cadastrar"),
    path('fornecedor/<int:pk>/', views.fornecedor_detail, name="fornecedor_detail"),
    path('fornecedor/<int:pk>/atualiza', views.fornecedor_atualiza, name="fornecedor_atualiza"),
    path('fornecedor/<int:pk>/delete', views.fornecedor_delete, name="fornecedor_delete"),
]
