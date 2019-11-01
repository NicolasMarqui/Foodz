from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cliente
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User, auth
from django.contrib import messages

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

    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        usuario = User.objects.filter(email=email)

        for i in usuario:
            user = auth.authenticate(username=i, password=senha)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Os dados não conferem')

    else:
        return render(request, 'login.html')

    return render(
        request,
        'login.html',
    )

def register(request):

    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Esse email ja existe')
        else:
            user = User.objects.create_user(username=nome, email=email, password=senha)
            user.save()
            return redirect('/login')

    return render(
        request,
        'register.html',
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

    cliente = Cliente.objects.all().filter(user_id=id)
    
    return render(
        request,
        'minha_conta.html',
        {
            "id": id,
            "cliente": cliente,
            "range": range(10)
        }
    )

def logout(request):
    django_logout(request)
    return redirect('/')