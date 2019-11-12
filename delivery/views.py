from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cliente, Produto, Restaurante, Notificacao, Carrinho, Favoritos, Placed_order
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User, auth, Group
from django.db.models import Q
from django.contrib import messages
from .forms import MoreInfoRestaurant, AddProducts, MoreInfoCliente
from django.shortcuts import get_object_or_404
import datetime
from django.http import JsonResponse
import json
from django.core import serializers
import requests

# Create your views here.
def home(request):

    produtos = Produto.objects.all().order_by('-id')[:10]
    restaurantes = Restaurante.objects.all()[:10]
    ta_nos_favoritos = []
    favoritos = None

    if not request.user.is_authenticated:
        favoritos = None

    if request.user.groups.filter(name="Donos").exists():
        favoritos = None

    try:
        id_user = Cliente.objects.get(user_id=request.user.id)
    except Cliente.DoesNotExist:
        id_user = None

    if id_user is not None:
        favoritos = Favoritos.objects.filter(id_cliente=id_user, is_favorito=1)

        for i in favoritos:
            ta_nos_favoritos.append(i.id_produto.nome)
    else:
        favoritos: None
        ta_nos_favoritos = []

    return render(
        request,
        'index.html',
        {
            'range': range(9),
            'range2': range(9),
            'produtos': produtos,
            'restaurantes': restaurantes,
            'favoritos': favoritos,
            'teste': ta_nos_favoritos
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

    produtos = Produto.objects.all().order_by('-id')

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

    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.groups.filter(name="Donos").exists():
        return redirect('/login')

    id = request.user.id

    info_restaurante = Restaurante.objects.filter(user_id = id)
    
    if info_restaurante:
        restaurante = Restaurante.objects.get(user_id = id)
        info_produtos = Produto.objects.filter(restaurante_id=restaurante.id)
    else:
        info_produtos = None

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

    info_restaurante = Restaurante.objects.filter(user_id = id)

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

        try:
            usuario = User.objects.filter(email=email)
        except User.DoesNotExist:
            usuario = None
            messages.info(request, 'O usuário não existe')

        try:
            has_login = User.objects.get(email=email)
        except User.DoesNotExist:
            has_login = None
            messages.info(request, 'O usuário não existe')

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

            new_cliente = Cliente(user_id=user.pk)
            new_cliente.save()

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

def restaurante_info(request,id = None):

    restaurante = Restaurante.objects.get(id=id)

    mais_produtos = Produto.objects.filter(restaurante_id=restaurante.id)[:4]

    return render(
        request,
        'restaurante_info.html',
        {
            'restaurante': restaurante,
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
    
    q_produtos = Produto.objects.filter(nome__icontains=query)
    q_restaurantes = Restaurante.objects.filter(nome__icontains=query)

    print(q_produtos)

    return render(
        request,
        'pesquisa.html',
        {
            'query': query,
            'produtos': q_produtos,
            'restaurantes': q_restaurantes,
        }
    )

def minha_conta(request, id):

    msg = ''
    success = False
    items = ''
    data = ''

    if not request.user.is_authenticated:
        return redirect('/dashboard')

    if request.user.groups.filter(name="Donos").exists():
        return redirect('/dashboard')

    try:
        cliente = Cliente.objects.filter(user_id=id)
        success = True

    except Cliente.DoesNotExist:
        msg = 'Erro ao encontrar o cliente'

    try:
        items = Placed_order.objects.filter(id_cliente=id)

        if not items:
            msg = 'Nenhum pedido encontrado'

    except Placed_order.DoesNotExist:
        items = None
        msg = 'Nenhum pedido encontrado'

    #Cadastro
    #Pegar dados existentes
    try:
        cliente = Cliente.objects.filter(user_id=id)

        for i in cliente:
            data = {
                'user': request.user.username,
                'cpf': i.cpf,
                'telefone': i.telefone,
                'avatar': i.avatar,
                'user_id': i.user_id
            }

        form = MoreInfoCliente(request.POST or None, request.FILES or None, initial=data, instance=cliente.first())
    except Cliente.DoesNotExist:
        form = MoreInfoCliente(request.POST or None, request.FILES or None)

    #Salvar os dados
    if request.method == 'POST':
        if form.is_valid():
            form.save()

    return render(
        request,
        'minha_conta.html',
        {
            "id": id,
            "cliente": cliente,
            'msg': msg,
            'pedidos': items,
            'form': form
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

def get_produto_editar(request):

    id_produto = request.POST['id']
    id_user = request.user.id

    if request.method == 'POST' and request.is_ajax():

        produto = Produto.objects.filter(id=id_produto)

        for i in produto:
            data = {
                'id': i.id,
                'nome': i.nome,
                'foto': i.foto,
                'descricao': i.descricao,
                'ingredientes': i.ingredientes,
                'preco': i.preco,
                'ativo': i.ativo,
                'categoria': i.categoria,
                'restaurante_id': i.restaurante_id,
            }

            instance = Produto.objects.get(id=id_produto)
            form = AddProducts(request.FILES or None,initial=data ,instance=instance)

            return HttpResponse(form.as_p())
            # return JsonResponse({ 'status': 'Success', 'form': form})
    
    else:
         return JsonResponse({'status':'Fail', 'msg':'Request não é valido'})

def save_produto_editar(request):

    data = request.POST.get('data', False)
    id = request.POST.get('id', False)

    if request.method == 'POST' and request.is_ajax():

        form_data_dict = {}
        form_data_list = json.loads(data)

        prod = Produto.objects.get(id=id)

        for field in form_data_list:
            form_data_dict[field["name"]] = field["value"]
            print(field["name"])

        if form_data_dict["ativo"] == 'on':
            ativo = True
        else:
            ativo = False

        prod.nome           = form_data_dict["nome"]
        prod.categoria      = form_data_dict["categoria"]
        prod.restaurante    = prod.restaurante
        prod.descricao      = form_data_dict["descricao"]
        prod.ingredientes   = form_data_dict["ingredientes"]
        prod.preco          = form_data_dict["preco"]
        prod.ativo          = ativo
        
        prod.save()

        return JsonResponse({ 'status': 'success', 'id': id})


def produtos_todos(request):
    rest = Restaurante.objects.get(user_id=request.user.id)
    produtos = list(Produto.objects.filter(restaurante_id = rest.id).values())

    data = dict()
    data['produtos'] = produtos
    print(produtos)

    return JsonResponse(data)

def produtos_editar(request, id):

    # prod = Restaurante.objects.get(id=id)

    # produtos = list(Produto.objects.filter(restaurante_id = rest.id).values())

    # data = dict()
    # data['produtos'] = produtos
    # print(produtos)

    # return JsonResponse(data)
    pass

def promocoes(request):
    return render(
        request,
        'promocoes.html',
    )

def carrinho_add(request):
    
    if request.method == 'POST' and request.is_ajax():

        if not request.user.is_authenticated:
            return JsonResponse({ 'status': 'error', 'msg': 'Você deve estar logado para realizar essa ação'})

        if request.user.groups.filter(name="Donos").exists():
            return JsonResponse({ 'status': 'error', 'msg': 'Donos de restaurante não podem efetuar essa ação'})

        #Id do produto
        id = request.POST['id']

        #Instancia do produto e do cliente
        id_produto = Produto.objects.get(id=id)
        id_user = Cliente.objects.get(user_id=request.user.id)

        #Verifica se o item ja esta no carrinho   
        try:
            is_item = Carrinho.objects.get(id_produto=id_produto)
        except Carrinho.DoesNotExist:
            is_item = None

        if is_item is not None:
            quantidade = is_item.quantidade
            is_item.quantidade = quantidade + 1

            is_item.save()

            msg = 'Mais uma unidade de {} adicionada ao carrinho'.format(is_item.id_produto.nome)

            return JsonResponse({ 'status': 'success', 'msg': msg, 'qnt_carrinho': is_item.quantidade, 'ja_tem': True})

        else:
            #Cria uma instancia do carrinho
            item = Carrinho(id_cliente=id_user, id_produto=id_produto, is_carrinho=1)

            #Salva o produto no carrinho
            item.save()

            todos_no_carrinho = Carrinho.objects.filter(id_cliente=id_user, is_carrinho=1)

            prod = Produto.objects.get(id=id)

            msg = '{} adicionado ao carrinho'.format(prod.nome)

            return JsonResponse({ 'status': 'success', 'msg': msg, 'qnt_carrinho': todos_no_carrinho.count()})

def carrinho_todos(request):

    if request.method == 'GET' and request.is_ajax():

        if not request.user.is_authenticated:
            msg = 'Você ainda não possui item! Faça o login para adicionar produtos'
            return JsonResponse({ 'status': 'sucess', 'qnt_items': 0, 'msg': msg, 'empty': True},json_dumps_params={'ensure_ascii': False},safe=False)

        if request.user.groups.filter(name="Donos").exists():
            msg = 'Você ainda não possui item! Crie uma conta como cliente para adicionar produtos'
            return JsonResponse({ 'status': 'error', 'qnt_items': 0, 'msg': msg, 'empty': True})

        
        try:
            #Inicializa dictionario
            data = dict()

            #Pega id do usuario
            id_user = Cliente.objects.get(user_id=request.user.id)
            
            #Pega os valores
            produtos_carrinho = list(Carrinho.objects.filter(id_cliente=id_user.id, is_carrinho=1).values()) 

            #Add info to JSON
            data['produtos'] = produtos_carrinho
            data['status'] = 'success'
            data['qnt_items'] = 0
            data['msg'] = 'null'
            info_prod = []
            total = 0

            # prod_nome = Produto.objects.filter(id=id)

            if produtos_carrinho:
                for i in produtos_carrinho:
                    print(i['id'])
                    prod = Produto.objects.filter(id=i['id_produto_id'])

                    for j in prod:

                        total += (j.preco * i['quantidade'])

                        info = {
                            'nome': j.nome,
                            'preco': j.preco,
                            'restaurante': j.restaurante.nome,
                        }

                        info_prod.append(info)
                        print(i)
                        data['info'] = list(info_prod)
                        data['total'] = total

            return JsonResponse(data)
        except Cliente.DoesNotExist:
            return JsonResponse({'empty': True})


def carrinho_excluir(request):
    if request.method == 'POST' and request.is_ajax():
        
        id = request.POST['id']

        try:
            item = Carrinho.objects.get(id=id)
            item.delete()

            print(item)

            msg = '{} excluido com sucesso'.format(item.id_produto.nome)
            return JsonResponse({ 'status': 'success' , 'msg': msg})

        except Carrinho.DoesNotExist:
            return JsonResponse({'status': 'error', 'msg': 'Erro ao deletar o produto'})

def carrinho(request):

    if not request.user.is_authenticated:
        msg = 'Você tem que estar logado para ver os items no carrinho'
        success = None
        preco_carrinho = 0
        item = None
        taxa_entrega = 0
        msg_entrega = []
        final = 0

    if request.user.groups.filter(name="Donos").exists():
        msg = 'Você tem que ser cliente para ver os items no carrinho'
        success = None
        preco_carrinho = 0
        item = None
        taxa_entrega = 0
        msg_entrega = []
        final = 0

    try:
        id_user = Cliente.objects.get(user_id=request.user.id)
    except Cliente.DoesNotExist:
        id_user = None
        item = None
        taxa_entrega = 0
        msg_entrega = []
        final = 0
        success = None

    if id_user is not None:
        try:
            item = Carrinho.objects.filter(id_cliente=id_user, is_carrinho=1)
            success = True
            msg = None
            preco_carrinho = 0
            taxa_entrega = 0
            msg_entrega = []
            final = 0

            for index, i in enumerate(item, start=1):

                if index >= 1 and i.id_produto.restaurante.nome != i.id_produto.restaurante.nome:
                    msg_entrega.append("Restaurante {} possui taxa de entrega de R${}".format(i.id_produto.restaurante.nome, i.id_produto.restaurante.taxa_entrega))
                    taxa_entrega += i.id_produto.restaurante.taxa_entrega
                else:
                    msg_entrega.append("Restaurante {} possui taxa de entrega de R${}".format(i.id_produto.restaurante.nome, i.id_produto.restaurante.taxa_entrega))
                    taxa_entrega = i.id_produto.restaurante.taxa_entrega

                preco_carrinho += (i.id_produto.preco * i.quantidade)

            final = preco_carrinho + taxa_entrega

        except Carrinho.DoesNotExist:
            item = None
            success = None
            msg = 'Nenhum item no carrinho'
            preco_carrinho = 0
            taxa_entrega = 0
            msg_entrega = []
            final = 0

    
    return render(
        request,
        'carrinho.html',
        {
            'msg': msg,
            'success': success,
            'produtos': item,
            'preco_carrinho': preco_carrinho,
            'taxa': taxa_entrega,
            'msg_entrega': msg_entrega,
            'final': final
        }
    )

def carrinho_cep(request):
    if request.method == 'POST' and request.is_ajax():
        if not request.user.is_authenticated:
            msg = 'Você tem que estar logado para calcular o CEP'
            return JsonResponse({ 'status': 'erro' , 'msg': msg})

        if request.user.groups.filter(name="Donos").exists():
            msg = 'Você tem que ser cliente para calcular o CEP'
            return JsonResponse({ 'status': 'erro' , 'msg': msg})

        try:
            id_user = Cliente.objects.get(user_id=request.user.id)
        except Cliente.DoesNotExist:
            id_user = None

        if id_user is not None:
            cep_user = request.POST['cep']
            try:
                item = Carrinho.objects.filter(id_cliente=id_user, is_carrinho=1).distinct()
                success = True
                msg = None
                preco = 0

                for i in item:
                    # print(i.id_produto.restaurante.cep)
                    url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?“nCdEmpresa=''&sDsSenha=''&sCepOrigem={}&sCepDestino={}&nVlPeso=1&nCdFormato=1&nVlComprimento=20&nVlAltura=5&nVlLargura=15&nCdServico=41106&StrRetorno=xml".format(i.id_produto.restaurante.cep, cep_user)
                    r = requests.get(url, data=request.GET)

                msg = 'Teste'
                return JsonResponse({ 'status': 'success' , 'msg': msg, 'cep': json.dumps(r.text)}, json_dumps_params={'ensure_ascii': False},safe=False)

            except Carrinho.DoesNotExist:
                msg = 'Erro ao calcular o CEP'
                return JsonResponse({ 'status': 'erro' , 'msg': msg})
        else:
            msg = 'Erro ao calcular o CEP'
            return JsonResponse({ 'status': 'erro' , 'msg': msg})

def favoritos_add(request):
    if request.method == 'POST' and request.is_ajax():
        id = request.POST['id']
        if not request.user.is_authenticated:
            msg = 'Você tem que estar logado para adicionar aos favoritos'
            return JsonResponse({ 'status': 'erro' , 'msg': msg})

        if request.user.groups.filter(name="Donos").exists():
            msg = 'Você tem que ser cliente para adicionar aos favoritos'
            return JsonResponse({ 'status': 'erro' , 'msg': msg})

        try:
            id_user = Cliente.objects.get(user_id=request.user.id)
        except Cliente.DoesNotExist:
            id_user = None

        try:
            id_produto = Produto.objects.get(id=id)
        except Produto.DoesNotExist:
            id_produto = None

        try:
            already_exists = Favoritos.objects.get(id_produto=id_produto)
        except Favoritos.DoesNotExist:
            already_exists = None
        

        if id_user is not None and already_exists is None:
            fav = Favoritos(is_favorito=1, id_cliente=id_user, id_produto=id_produto)
            fav.save()

            try:
                just_added = Favoritos.objects.get(id_produto=id)
                msg = '{} adicionado aos favoritos'.format(just_added.id_produto.nome)
            except:
                msg = 'Adicionado aos favoritos'
                just_added = None

            return JsonResponse({ 'status': 'success' , 'msg': msg})
        else:
            msg = 'Erro ao adicionar aos favoritos'
            return JsonResponse({ 'status': 'erro' , 'msg': msg})

def favoritos_remove(request):
    if request.method == 'POST' and request.is_ajax():
        id = request.POST['id']
        if not request.user.is_authenticated:
            msg = 'Como assim você conseguiu adicionar algo nos favoritos?'
            return JsonResponse({ 'status': 'erro' , 'msg': msg})

        if request.user.groups.filter(name="Donos").exists():
            msg = 'Como assim você conseguiu adicionar algo nos favoritos?'
            return JsonResponse({ 'status': 'erro' , 'msg': msg})

        try:
            id_user = Cliente.objects.get(user_id=request.user.id)
        except Cliente.DoesNotExist:
            id_user = None

        try:
            id_produto = Produto.objects.get(id=id)
        except Produto.DoesNotExist:
            id_produto = None

        try:
            already_exists = Favoritos.objects.get(id_produto=id_produto)
        except Favoritos.DoesNotExist:
            already_exists = None
        

        if id_user is not None and already_exists is not None:
            fav = Favoritos.objects.get(id_cliente=id_user, id_produto=id_produto)
            fav.delete()

            try:
                just_removed = Produto.objects.get(id=id)
                msg = '{} removido dos favoritos'.format(just_removed.nome)
            except:
                msg = 'Removido dos favoritos'
                just_removed = None

            return JsonResponse({ 'status': 'success' , 'msg': msg})
        else:
            msg = 'Erro ao remover dos favoritos'
            return JsonResponse({ 'status': 'erro' , 'msg': msg})

def checkout(request):

    msg = ''
    items = ''
    success = ''
    total = 0
    taxa_entrega = 0
    final = 0

    if not request.user.is_authenticated:
        msg = 'Para de digitar na URL e cria uma conta logo'
        success = False

    if request.user.groups.filter(name="Donos").exists():
       msg = 'Para de digitar na URL e cria uma conta logo'
       success = False

    try:
        id_user = Cliente.objects.get(user_id=request.user.id)
    except Cliente.DoesNotExist:
        id_user = None
    
    #Pega os items que estão no carrinho
    try:
        items = Carrinho.objects.filter(id_cliente=id_user.id)
        success = True
        msg = None

        for i in items:
            total += i.id_produto.preco
            taxa_entrega += i.id_produto.restaurante.taxa_entrega
    
        final = total + taxa_entrega

    except Carrinho.DoesNotExist:
        items = None

    return render(
        request,
        'checkout.html',
        {
            'items': items,
            'success': success,
            'msg': msg,
            'total': total,
            'taxa_entrega': taxa_entrega,
            'final': final
        }
    )