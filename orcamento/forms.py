from datetime import date


from django import forms
from .models import Clientes

class ClienteForm(forms.ModelForm):
	class Meta:
		model = Clientes
		#fields = [
		#	"nome",
		#	"telefone",
		#	"telefone2",
		#	"contato",
		#	"email",
		#	"email2",
		#	"obs",
		#]
		fields = "__all__"
		widgets = {
			'data_ultimo': forms.DateInput(
				attrs={'type':'date'}
				), 
			'data_criacao': forms.DateInput(
				attrs={'type': 'date'}
				)
		}
	def __init__(self, *args, **kwargs):
		super(ClienteForm, self).__init__(*args, **kwargs)
		#self.fields['criador'].disabled = True
		#self.fields['data_criacao'].disabled = True
		#self.fields['data_ultimo'].disabled = True
		#self.fields['data_ultimo'].
	"""nome = forms.CharField(max_length=250)
	telefone = forms.CharField(max_length=20, required=False)
	telefone2 = forms.CharField(max_length=20, required=False)
	contato = forms.CharField(max_length=250, required=False)
	email = forms.EmailField(max_length=250, required=False)
	email2 = forms.EmailField(max_length=250, required=False)
	obs = forms.CharField(widget=forms.Textarea, required=False)


	criador = forms.IntegerField(widget=forms.HiddenInput(), required=False)
	data_criacao = forms.IntegerField(widget=forms.HiddenInput(), required=False)
	data_ultimo = forms.IntegerField(widget=forms.HiddenInput(), initial=date.today())"""