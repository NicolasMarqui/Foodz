from django.shortcuts import render
from django.http import HttpResponse

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
    return render(
        request,
        'login.html',
    )

def produto_info(request,id = None):
    return render(
        request,
        'produto_info.html',
        {
            'range': range(5),
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