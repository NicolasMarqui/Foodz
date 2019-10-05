from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Cidade(models.Model):
    nomeCidade = models.CharField(max_length=255)

class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    cidade = models.ForeignKey(Cidade, on_delete = models.CASCADE)
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=255)
    cep = models.CharField(max_length=10)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    senha = models.CharField(max_length=50)
    cadastro_criado = models.DateTimeField()
    is_dono = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="pics/clientes/", default='pics/None/no-img.png')
    ultimo_compra = models.DateTimeField(auto_now=True)
    quantidade_comentarios = models.IntegerField(blank=True)

class Restaurante(models.Model):
    nome = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="pics/restaurante/", default='pics/None/no-img.png')
    endereco = models.CharField(max_length=255)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    vendas = models.IntegerField(blank=True)

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="pics/produtos/", default='pics/None/no-img.png')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    descricao = models.TextField()
    ingredientes = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=5,decimal_places=2)
    ativo = models.BooleanField(default=True)

class Oferta(models.Model):
    inicio_data_oferta = models.DateField(null=True)
    inicio_horario_oferta = models.TimeField(null=True)
    fim_data_oferta = models.DateField(null=True)
    fim_horario_oferta = models.TimeField(null=True)
    preco_oferta = models.DecimalField(max_digits=5,decimal_places=2)

class Em_Oferta(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

class Comentario(models.Model):
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto_id = models.ForeignKey(Produto, on_delete=models.CASCADE)
    restaurante_id = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    nota = models.PositiveIntegerField(null=True,default=0 ,validators=[MinValueValidator(0),MaxValueValidator(5)])
    descricao = models.TextField(blank=True)
    recomenda = models.BooleanField(default=True)
    data_comentario = models.DateTimeField()
