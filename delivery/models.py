from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Cidade(models.Model):
    nomeCidade = models.CharField(max_length=255, choices=CIDADES_CHOICE)

    def __str__(self):
        return '{}' .format(self.nomeCidade)

class Endereco(models.Model):
    id_cliente                  = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    cep                         = models.CharField(max_length=10)
    endereco                    = models.CharField(max_length=255)
    numero                      = models.CharField(max_length=255, blank=True, null=True)
    complemento                 = models.CharField(max_length=100, blank=True, null=True)
    tipo                        = models.CharField(max_length=255, choices=TIPO_CHOICE)
    cidade                      = models.ForeignKey(Cidade, on_delete = models.CASCADE)

    def __str__(self):
        return '{} e {}' .format(self.id_cliente, self.endereco)

class Cliente(models.Model):
    user                        = models.OneToOneField(User, on_delete=models.CASCADE)
    endereco_id                 = models.ForeignKey(Endereco, on_delete = models.CASCADE,blank=True,null=True)
    cpf                         = models.CharField(max_length=14,blank=True)
    telefone                    = models.CharField(max_length=30,blank=True)
    cadastro_criado             = models.DateTimeField(auto_now=True)
    avatar                      = models.ImageField(upload_to="pics/clientes/", default='pics/None/no-img.png',blank=True, null=True)
    ultimo_compra               = models.DateTimeField(auto_now=True,blank=True)
    quantidade_comentarios      = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return 'ID: {} e username: {} '.format(self.id, self.user.username)

class Restaurante(models.Model):
    user                        = models.OneToOneField(User, on_delete=models.CASCADE)
    nome                        = models.CharField(max_length=100)
    cep                         = models.CharField(max_length=10)
    estado                      = models.CharField(max_length=255)
    cidade                      = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    endereco                    = models.CharField(max_length=255)
    numero                      = models.CharField(max_length=255)
    complemento                 = models.CharField(max_length=255,blank=True, null=True)
    especialidade               = models.CharField(max_length=255, choices=ESPECIALIDADE_CHOICE)
    razao_social                = models.CharField(max_length=255)
    total_vendas                = models.IntegerField(blank=True)
    descricao                   = models.CharField(max_length=255)
    logo                        = models.ImageField(upload_to="pics/restaurantes", default='pics/None/no-img.png')
    cnpj                        = models.CharField(max_length=18)
    taxa_entrega                = models.DecimalField(max_digits=5,decimal_places=2,default=5)

    def __str__(self):
        return 'ID: {} e nome: {} '.format(self.id, self.nome)


class Categoria(models.Model):
    categoria                   = models.CharField(max_length=255, choices=CATEGORIAS_CHOICES)

    def __str__(self):
        return 'categoria: {} '.format(self.categoria)

class Produto(models.Model):
    nome                        = models.CharField(max_length=100)
    foto                        = models.ImageField(upload_to="pics/produtos/", default='pics/None/no-img.png')
    categoria                   = models.CharField(max_length=255, choices=CATEGORIAS_CHOICES)
    restaurante                 = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    descricao                   = models.TextField()
    ingredientes                = models.TextField(blank=True)
    preco                       = models.DecimalField(max_digits=5,decimal_places=2)
    ativo                       = models.BooleanField(default=True)
    nota                        = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return 'ID: {} e nome: {} '.format(self.id, self.nome)

class Oferta(models.Model):
    inicio_data_oferta          = models.DateField(null=True)
    inicio_horario_oferta       = models.TimeField(null=True)
    fim_data_oferta             = models.DateField(null=True)
    fim_horario_oferta          = models.TimeField(null=True)
    preco_oferta                = models.DecimalField(max_digits=5,decimal_places=2)

class Em_Oferta(models.Model):
    oferta                      = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    produto                     = models.ForeignKey(Produto, on_delete=models.CASCADE)

class Comentario(models.Model):
    cliente_id                  = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto_id                  = models.ForeignKey(Produto, on_delete=models.CASCADE)
    restaurante_id              = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    nota                        = models.PositiveIntegerField(null=True,default=0 ,validators=[MinValueValidator(0),MaxValueValidator(5)])
    descricao                   = models.TextField(blank=True)
    recomenda                   = models.BooleanField(default=True)
    data_comentario             = models.DateTimeField()

class Placed_order(models.Model):
    id_restaurante              = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    order_time                  = models.DateTimeField(auto_now=True,)
    tempo_estimado              = models.IntegerField(blank=True, default=15)
    comida_pronta               = models.DateTimeField(auto_now=True, blank=True)
    endereco_entrega            = models.CharField(max_length=255)
    endereco_saida              = models.CharField(max_length=255)
    id_cliente                  = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_produto                  = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade                  = models.IntegerField(default=1)
    comentario                  = models.TextField(blank=True, null=True)

class Compras(models.Model):
    id_cliente                  = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_produto                  = models.ForeignKey(Produto, on_delete=models.CASCADE)
    id_restaurante              = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    placed_order_id             = models.ForeignKey(Placed_order, on_delete=models.CASCADE)

class Notificacao(models.Model):
    id_user                     = models.ForeignKey(User, on_delete=models.CASCADE)
    mensagem                    = models.TextField(blank=True, null=True)
    foi_lida                    = models.BooleanField(default=False)
    lixeira                     = models.BooleanField(default=False)
    data_comentario             = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return 'user_id: {} e mensagem: {}'.format(self.id_user, self.mensagem)

class Carrinho(models.Model):
    id_cliente                  = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_produto                  = models.ForeignKey(Produto, on_delete=models.CASCADE)
    adicionado_carrinho         = models.DateTimeField(auto_now=True,blank=True)
    quantidade                  = models.IntegerField(default=1)
    is_carrinho                 = models.BooleanField(default=False)

class Favoritos(models.Model):
    id_cliente                  = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_produto                  = models.ForeignKey(Produto, on_delete=models.CASCADE)
    is_favorito                 = models.BooleanField(default=False)
    adicionado_favorito         = models.DateTimeField(auto_now=True,blank=True)