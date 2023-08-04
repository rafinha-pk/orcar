from datetime import date


from django import forms
from .models import Clientes
from .models import Fornecedores
from .models import Produtos
from .models import Orcamentos

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

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = "__all__"
        widgets = {
            'data_ultimo': forms.DateInput(
                attrs={'type':'date'}
                ), 
            'data_criacao': forms.DateInput(
                attrs={'type': 'date'}
                ),
            'valor_fornecedor': forms.DateInput(
                attrs={'placeholder': 'R$ '}
                ),
            'valor_final': forms.DateInput(
                attrs={'placeholder': 'R$ '}
                ),
            'margem': forms.DateInput(
                attrs={'placeholder': '% '}
                ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class']=  'form-control'
        self.fields['valor_fornecedor'].widget.attrs['class'] += ' money'
        self.fields['valor_final'].widget.attrs['class'] += ' money'
        self.fields['margem'].widget.attrs['class'] += ' margem'

class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamentos
        fields = "__all__"
        widgets = {
            'data_ultimo': forms.DateInput(
                attrs={'type':'date'}
                ), 
            'data_criacao': forms.DateInput(
                attrs={'type': 'date'}
                ),
            'data_vencimento': forms.DateInput(
                attrs={'type': 'date'}
                ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class']=  'form-control'