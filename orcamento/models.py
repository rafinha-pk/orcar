from django.db import models
from django.contrib.auth.models import User

class Clientes(models.Model):
	# clientes
	nome = models.CharField(max_length=250)
	telefone = models.CharField(max_length=20, blank=True)
	telefone2 = models.CharField(max_length=20, blank=True)
	contato = models.CharField(max_length=250, blank=True)
	email = models.EmailField(max_length=250, blank=True)
	email2 = models.EmailField(max_length=250, blank=True)
	criador = models.ForeignKey(User, blank=True, on_delete=models.SET(''))
	data_criacao = models.DateField('Data do cadastro')
	data_ultimo = models.DateField('Ultima atividade')
	obs = models.TextField(blank=True)

	def __str__(self):
		return self

class Fornecedores(models.Model):
	nome = models.CharField(max_length=250)
	telefone = models.CharField(max_length=20, blank=True)
	telefone2 = models.CharField(max_length=20, blank=True)
	contato = models.CharField(max_length=250, blank=True)
	email = models.EmailField(max_length=250, blank=True)
	email2 = models.EmailField(max_length=250, blank=True)
	criador = models.ForeignKey(User, blank=True, on_delete=models.SET(''))
	data_criacao = models.DateField('Data do cadastro')
	data_ultimo = models.DateField('Ultima atividade')
	obs = models.TextField(blank=True)

	def __str__(self):
		return self

class Produtos(models.Model):
	nome = models.CharField(max_length=250)
	pn = models.CharField(max_length=200, blank=True)
	lista_unidade = [
		('Un', 'Unidade'),
		('Cx', 'Caixa'),
		('Pc', 'Peça'),
		('Pt', 'Pacote'),
		('Kt', 'Kit'),
		('Kg', 'Quilo'),
		('Gr', 'Grama'),
		('Mt', 'Metro'),
		('Cm', 'Centimetro')
	]
	unidade = models.CharField(max_length=3, choices=lista_unidade, blank=True)
	valor_fornecedor = models.DecimalField(max_digits = 10, decimal_places = 2, blank=True)
	valor_final = models.DecimalField(max_digits = 10, decimal_places = 2, blank=True)
	margem = models.DecimalField(max_digits = 5, decimal_places = 2, blank=True)
	fornecedor = models.ForeignKey(Fornecedores, blank=True, on_delete=models.SET(''))
	criador = models.ForeignKey(User, blank=True, on_delete=models.SET(''))
	data_criacao = models.DateField('Data do cadastro')
	data_ultimo = models.DateField('Ultima atividade')
	obs = models.TextField(blank=True)

	def __str__(self):
		return self

class StatusOrcamento(models.Model):
	nome = models.CharField(max_length=100)

	def __str__(self):
		return self.nome

class FormaPagamento(models.Model):
	nome = models.CharField(max_length=100)

	def __str__(self):
		return self

class Orcamentos(models.Model):

	criador = models.ForeignKey(User, blank=True, on_delete=models.SET(''))
	cliente = models.ForeignKey(Clientes, blank=True, on_delete=models.SET(''))
	data_criacao = models.DateTimeField("Criação")
	data_ultimo = models.DateTimeField('Ultima atividade')
	data_vencimento = models.DateField('Vencimento')
	quantidade = models.IntegerField(blank=True, default=0)
	valor_custo = models.DecimalField(max_digits = 10, decimal_places = 2, blank=True)
	valor_final = models.DecimalField(max_digits = 10, decimal_places = 2, blank=True)
	margem = models.DecimalField(max_digits = 5, decimal_places = 2, blank=True)
	status = models.ForeignKey(StatusOrcamento, blank=True, on_delete=models.SET(''))
	pagamento = models.ForeignKey(FormaPagamento, blank=True, on_delete=models.SET(''))
	parcelas = models.IntegerField(blank=True, default=1)
	obs = models.TextField(blank=True)
	def __str__(self):
		return self

class RegOrcamentos(models.Model):
	orcamento = models.ForeignKey(Orcamentos, on_delete=models.CASCADE)
	produto = models.ForeignKey(Produtos, blank=True, on_delete=models.SET(''))
	quantidade = models.IntegerField(blank=True)
	fornecedor = models.ForeignKey(Fornecedores, blank=True, on_delete=models.SET(''))
	valor_custo = models.DecimalField(max_digits= 10, decimal_places = 2, blank=True)
	valor_final = models.DecimalField(max_digits= 10, decimal_places = 2, blank=True)
	margem = models.DecimalField(max_digits = 5, decimal_places = 2, blank=True)
	data = models.DateTimeField("Data")

	def __str__(self):
		return self
