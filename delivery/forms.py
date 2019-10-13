from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *

class CreateNewUser(forms.Form):
    nome                        = forms.CharField(max_length=50, label="Nome", required=True,error_messages={'required': 'Por Favor digite seu nome'})
    email                       = forms.EmailField(required=True)
    senha                       = forms.CharField(max_length=50, widget=forms.PasswordInput(),required=True)
    cpf                         = forms.CharField(max_length=14, required=True)
    telefone                    = forms.CharField(max_length=30, required=True)

class LoginUser(forms.Form):
    email                       = forms.EmailField(required=True)
    senha                       = forms.CharField(max_length=50, widget=forms.PasswordInput(), required=True)