from django import forms
from .models import Clientes

class ClienteForm(forms.ModelForm):
	class Meta:
		model = Clientes
		fields = [
			"nome",
			"telefone",
			"telefone2",
			"contato",
			"email",
			"email2",
			"obs",
		]
	criador = forms.IntegerField(widget=forms.HiddenInput(), required=False)
	data_criacao = forms.IntegerField(widget=forms.HiddenInput(), required=False)
	data_ultimo = forms.IntegerField(widget=forms.HiddenInput(), required=False)