from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cliente, Produto, Restaurante, Notificacao
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User, auth, Group
from django.db.models import Q
from django.contrib import messages
from .forms import MoreInfoRestaurant, AddProducts
from django.shortcuts import get_object_or_404
import datetime
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
def home(request):

    # if request.user.is_authenticated and not request.user.groups.filter(name="Donos").exists():
    #     P

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

    produtos = Produto.objects.all()

    return render(
        request,
        'produtos.html',
        {
            'range': range(9),
            'produtos': produtos
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

    info_restaurante = Restaurante.objects.get(user_id = id)
    info_produtos = Produto.objects.filter(restaurante_id=info_restaurante.id)

    print(info_restaurante.id)
    
    return render(
        request,
        'dashboard.html',
        {
            'range': range(9),
            'info': info_restaurante,
            'ult_produtos': info_produtos,
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

    id = request.user.id

    info_restaurante = Restaurante.objects.get(user_id = id)

    if info_restaurante:

        rest = Restaurante.objects.get(user_id = id)

        data = {
            'restaurante': rest.id
        }


        form = AddProducts(request.POST or None, request.FILES or None ,initial=data)
        produtos = Produto.objects.filter(restaurante_id=rest.id)
    
    else:
        form = None
        produtos = None
        print('deu ruim')

    print(form.is_valid())
    if request.method == 'POST':
        if form.is_valid():
            nome = request.POST['nome']
            novo_produto = form.save()


            mensagem = 'Parabéns, você adicionou o produto {} !'.format(nome)
            notificacao = Notificacao(id_user=request.user, mensagem=mensagem)
            notificacao.save()

            return redirect('/dashboard/')

    return render(
        request,
        'dashboard_produtos.html',
        {
            'range': range(9),
            'form': form,
            'produtos': produtos
        }
    )

def dashboard_config(request):

    id = request.user.id

    info_restaurante = Restaurante.objects.filter(user_id = id)

    if info_restaurante:

        first_time = False

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
            form = MoreInfoRestaurant( request.POST or None, request.FILES or None ,initial=data ,instance=instance)

    else:
        first_time = True
        form = MoreInfoRestaurant(request.POST, request.FILES or None)


    if request.method == 'POST':
        if form.is_valid():
            if info_restaurante:
                novo_restaurante = form.save()
                msg = "Seu perfil foi alterado com sucesso!"
                notificacao = Notificacao(id_user=request.user, mensagem=msg)
                notificacao.save()

            else:
                novo_restaurante = form.save(commit=False)
                novo_restaurante.user_id = request.user.id
                novo_restaurante.total_vendas = 0

            novo_restaurante.save()
            return redirect('/dashboard/')
            
    return render(
        request,
        'dashboard_config.html',
        {
            'range': range(9),
            'info': info_restaurante,
            'form': form,
            'first_time': first_time,
        }
    )

def login(request):

    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        usuario = User.objects.filter(email=email)

        has_login = User.objects.get(email=email)

        if usuario.exists():
            for i in usuario:
                user = auth.authenticate(username=i, password=senha)
        else:
            user = None

        if user is not None:

            if has_login.last_login == 'NULL':
                notificacao = Notificacao(id_user=has_login, mensagem="Bem vindo ao nosso sistema")
                notificacao.save()
            else:
                msg = "Bem Vindo novamente, Sentimos sua falta!"
                # notificacao = Notificacao(id_user=has_login, mensagem=msg)
                # notificacao.save()

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

            return redirect('/login')

    return render(
        request,
        'register.html',
    )

def produto_info(request,id = None):

    produto = Produto.objects.get(id=id)

    mais_produtos = Produto.objects.filter(restaurante_id=produto.restaurante.id)[:2]

    return render(
        request,
        'produto_info.html',
        {
            'nota': str(produto.nota),
            'produto': produto,
            'mais_produtos': mais_produtos
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
        }
    )

def logout(request):
    django_logout(request)
    return redirect('/')

def lida(request):

    id = request.POST['id']

    print(id)

    if request.method == 'POST' and request.is_ajax():
        try:
            notificacao = Notificacao.objects.get(id=id)
            notificacao.foi_lida = request.POST['lida']

            not_faltando = Notificacao.objects.filter(id=id, foi_lida=0);
            data = list(not_faltando.values())

            notificacao.save()

            return JsonResponse({ 'status': 'Success', 'msg': 'Notificação foi lida' , 'notificacoes': data})

        except Notificacao.DoesNotExist:
            return JsonResponse({'status':'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status':'Fail', 'msg':'Request não é valido'})
