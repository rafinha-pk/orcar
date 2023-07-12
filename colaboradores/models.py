from django.db import models

class Colaboradores(models.Model):
	primeiro_nome = models.CharField(max_length=200)
	ultimo_nome = models.CharField(max_length=200)
	colaborador_usuario = models.CharField(max_length=100)
	email = models.EmailField(max_length=254)
	data_nascimento = models.DateField('Data de aniversario')
	data_inicio = models.DateField('Dadta de inicio')
	setor = models.ForeignKey(
		"Setores", on_delete=models.CASCADE, blank=True,
	)
	def __str__(self):
		return self.colaborador_usuario

class Setores(models.Model):
	setor_nome = models.CharField(max_length=200)
	descricao = models.TextField(blank=True)
	def __str__(self):
		return self.setor_nome
