from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from django.contrib.auth.forms import UserCreationForm
from .models import Restaurante

class MoreInfoRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = ['nome', 'cep', 'estado', 'cidade' , 'endereco' , 'numero' , 'complemento' , 'especialidade', 'razao_social', 'descricao', 'logo', 'cnpj']
