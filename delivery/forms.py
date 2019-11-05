from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from django.contrib.auth.forms import UserCreationForm
from .models import Restaurante, Produto
from django_summernote.widgets import SummernoteInplaceWidget,SummernoteWidget

class MoreInfoRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ['nome', 'cep', 'estado', 'cidade' , 'endereco' , 'numero' , 'complemento' , 'especialidade', 'razao_social', 'descricao', 'logo', 'cnpj']

        widgets = {
            'descricao': SummernoteWidget(),
        }

class AddProducts(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'foto', 'categoria' , 'restaurante' , 'descricao' , 'ingredientes' , 'preco' , 'ativo']

        widgets = {
            'restaurante': forms.TextInput(attrs={'readonly': 'readonly'}),
            'descricao': SummernoteWidget(),
            'ingredientes': SummernoteWidget(),
        }

        labels = {
            'restaurante': '',
        }

