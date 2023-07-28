from datetime import date


from django import forms
from .models import Clientes
from .models import Fornecedores

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
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
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class']=  'form-control'


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedores
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
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class']=  'form-control'
