from django.contrib import admin
from .models import Clientes, Fornecedores, Produtos, StatusOrcamento, FormaPagamento, Orcamentos, RegOrcamentos

admin.site.register(Clientes)
admin.site.register(Fornecedores)
admin.site.register(Produtos)
admin.site.register(StatusOrcamento)
admin.site.register(FormaPagamento)
admin.site.register(Orcamentos)
admin.site.register(RegOrcamentos)
