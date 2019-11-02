from django.contrib import admin
from .models import Cidade, Cliente, Endereco, Restaurante, Produto

# Register your models here.
admin.site.register(Cidade)
admin.site.register(Cliente)
admin.site.register(Endereco)
admin.site.register(Restaurante)
admin.site.register(Produto)