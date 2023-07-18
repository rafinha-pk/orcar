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
    path('cliente/', views.cliente_index),
    # path('cliente/<int:pk>/', views.cliente_detail),
    # path('fornecedor/', views.fornecedor_index),
    # path('fornecedor/<int:pk>/', views.fornecedor_detail),
    # path('produto/', views.produto_index),
    # path('produto/<int:pk>', views.produto_detail),
]
