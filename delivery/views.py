from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cliente, Produto, Restaurante, Notificacao
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User, auth, Group
from django.db.models import Q
from django.contrib import messages
from .forms import MoreInfoRestaurant
from django.shortcuts import get_object_or_404

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

    if(not request.user.is_authenticated):
        return redirect('/login')

    id = request.user.id

    info_restaurante = Restaurante.objects.filter(user_id = id)
    
    return render(
        request,
        'dashboard.html',
        {
            'range': range(9),
            'info': info_restaurante,
        }
    )

def dashboard_financeiro(request):
    return render(
        request,
        'dashboard_financeiro.html',
        {
            'range': range(9),
        }
    )

def dashboard_produtos(request):
    return render(
        request,
        'dashboard_produtos.html',
        {
            'range': range(9),
        }
    )

def dashboard_config(request):

    id = request.user.id

    info_restaurante = Restaurante.objects.filter(user_id = id)

    if info_restaurante:
        for i in info_restaurante:
            data = {
                'user': request.user.username,
                'nome': i.nome,
                'cep': i.cep,
                'estado': i.estado,
                'cidade': i.cidade,
                'endereco': i.endereco,
                'numero': i.numero,
                'complemento': i.complemento,
                'razao_social': i.razao_social,
                'descricao': i.descricao,
                'cnpj': i.cnpj,
            }

            instance = Restaurante.objects.get(user_id = request.user.id)
            form = MoreInfoRestaurant( request.POST or None, initial=data ,instance=instance)

    else:
        form = MoreInfoRestaurant(request.POST)


    if request.method == 'POST':
        if form.is_valid():
            if info_restaurante:
                novo_restaurante = form.save()
                print('eae')
            else:
                novo_restaurante = form.save(commit=False)
                novo_restaurante.user_id = request.user.id
                novo_restaurante.total_vendas = 0

            print(novo_restaurante)
            novo_restaurante.save()
            return redirect('/dashboard/')
            

    return render(
        request,
        'dashboard_config.html',
        {
            'range': range(9),
            'info': info_restaurante,
            'form': form
        }
    )

def login(request):

    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        usuario = User.objects.filter(email=email)

        print(usuario.exists())

        if usuario.exists():
            for i in usuario:
                user = auth.authenticate(username=i, password=senha)
        else:
            user = None

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
        nome    = request.POST['nome']
        email   = request.POST['email']
        senha   = request.POST['senha']
        tipo    = request.POST['tipo']

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Esse email ja existe')
        else:
            user = User.objects.create_user(username=nome, email=email, password=senha)
            user.save()

            if(tipo == 'Dono'):
                grupo_dono = Group.objects.get(name="Donos")
                grupo_dono.user_set.add(user)

            print(user)

            notificacao = Notificacao(id_user=request.user, mensagem="Bem vindo ao nosso sistema")
            notificacao.save()
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

    if request.user.groups.filter(name="Donos").exists():
        return redirect('/dashboard')
    
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