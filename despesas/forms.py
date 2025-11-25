from django import forms
from .models import Despesa

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        # Definimos quais campos o usuário vai preencher
        fields = ['descricao', 'valor', 'data', 'categoria', 'pago']
        
        # Um truque para o campo de data virar um calendário do navegador
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }