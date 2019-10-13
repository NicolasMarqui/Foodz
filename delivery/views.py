from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateNewUser, LoginUser
from .models import Cliente

# Create your views here.
def home(request):
    return render(
        request,
        'index.html',
        {
            'range': range(9),
            'range2': range(9),
        }
    )

def sobre_nos(request):
    return render(
        request,
        'sobre-nos.html',
        {
            'range': range(9),
        }
    )

def produtos(request):
    return render(
        request,
        'produtos.html',
        {
            'range': range(9),
        }
    )

def restaurantes(request):
    return render(
        request,
        'restaurantes.html',
        {
            'range': range(9)
        }
    )

def dashboard(request):
    return render(
        request,
        'dashboard.html',
        {
            'range': range(9),
        }
    )

def login(request):

    form = LoginUser()

    return render(
        request,
        'login.html',
        {
            "form": form,
        }
    )

def signup(request):

    form = CreateNewUser()

    return render(
        request,
        'signup.html',
        {
            "form": form,
        }
    )

def produto_info(request,id = None):
    return render(
        request,
        'produto_info.html',
        {
            'range': range(5),
            'id': id,
        }
    )

def cadastro_restaurantes(request):
    return render(
        request,
        'cadastro_restaurantes.html',
        {
            'range': range(5),
        }
    )

def pesquisa(request):

    query = request.POST['query']
    
    # q_produtos = Produto.objects.filter(nome__icontains=query)
    # q_restaurantes = Restaurante.objects.filter(Q(nome__icontains=query) | Q(endereco__icontains=query))

    return render(
        request,
        'pesquisa.html',
        {
            'query': query,
            # 'produtos': q_produtos,
            # 'restaurantes': q_restaurantes,
        }
    )

def minha_conta(request, id):

    cliente = Cliente.objects.all().filter(id=id)

    return render(
        request,
        'minha_conta.html',
        {
            "id": id,
            "cliente": cliente,
            "range": range(10)
        }
    )