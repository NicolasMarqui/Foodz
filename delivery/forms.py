from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from django.contrib.auth.forms import UserCreationForm
from .models import Restaurante, Produto, Cliente, Endereco
from django_summernote.widgets import SummernoteInplaceWidget,SummernoteWidget

class MoreInfoRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ['nome', 'cep', 'estado', 'cidade' , 'endereco' , 'numero' , 'complemento' , 'especialidade', 'razao_social', 'descricao', 'logo', 'cnpj']

        widgets = {
            'descricao': SummernoteWidget(),
        }

class MoreInfoCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cpf', 'telefone', 'avatar']

class AddProducts(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'foto', 'categoria' , 'restaurante' , 'descricao' , 'ingredientes' , 'preco' , 'ativo']

        widgets = {
            'id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'restaurante': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

        labels = {
            'restaurante': '',
        }

class AddAddress(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['id', 'cep', 'endereco', 'numero' , 'complemento' , 'tipo' , 'cidade']

        widgets = {
            'id': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

        labels = {
            'id': '',
        }
