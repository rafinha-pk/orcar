from django.contrib import admin
from django.urls import path
from orcamento import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.orcamento_index, name="home"),
    path('orcamento/cadastrar/<int:pk>/', views.orcamento_cadastra, name="orcamento_cadastra"),
    # path('orcamento/<int:pk>/', views.orcamento_detail),

    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

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

    path('produto/', views.produto_index, name="produto"),
    path('produto/cadastrar', views.produto_cadastra, name="produto_cadastrar"),
    path('produto/<int:pk>/', views.produto_detail, name="produto_detail"),
    path('produto/<int:pk>/atualiza', views.produto_atualiza, name="produto_atualiza"),
    path('produto/<int:pk>/delete', views.produto_delete, name="produto_delete"),
]
