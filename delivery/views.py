from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cliente, Produto, Restaurante, Notificacao, Carrinho, Favoritos, Placed_order, Endereco, Order, Status, Comentario
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User, auth, Group
from django.db.models import Q, Count
from django.contrib import messages
from .forms import MoreInfoRestaurant, AddProducts, MoreInfoCliente, AddAddress
from django.shortcuts import get_object_or_404
import datetime
from django.http import JsonResponse
import json
from django.core import serializers
import requests
from datetime import datetime
from django.utils import formats

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

    try:
        all_restaurante = Restaurante.objects.all()
    except Restaurante.DoesNotExist:
        all_restaurante = False


    return render(
        request,
        'restaurantes.html',
        {
            'restaurante': all_restaurante
        }
    )

def dashboard(request):

    #variaveis
    lucro = 0
    vendas = None
    ultimas_vendas = None

    #Verifica se user está logado
    if not request.user.is_authenticated:
        return redirect('/login')

    #Verifica se usuário é dono de restaurante
    if not request.user.groups.filter(name="Donos").exists():
        return redirect('/login')

    #Pega o ID
    id = request.user.id

    #Pega os dados do restaurante
    info_restaurante = Restaurante.objects.filter(user_id = id)
    
    if info_restaurante:
        restaurante = Restaurante.objects.get(user_id = id)

        #Ultimos produtos
        info_produtos = Produto.objects.filter(restaurante_id=restaurante.id)[:4]

        #Ultimas Vendas
        try:
            vendas = Placed_order.objects.filter(id_restaurante=restaurante.id)
            ultimas_vendas = Placed_order.objects.filter(id_restaurante=restaurante.id)[:4]
        except Placed_order.DoesNotExists:
            vendas = None
            ultimas_vendas = None

        #Salva total no restaurante
        if vendas is not None:
            restaurante.total_vendas = vendas.count()
            restaurante.save()

            #Pega o total de lucro
            for i in vendas:
                lucro += (i.id_produto.preco * i.quantidade)

            all_products_order = []
            soms = 0

            orders_sorted = Placed_order.objects.filter(id_restaurante=restaurante.id).values('id_produto').annotate(c=Count('id_produto')).order_by('-c')[:6]

            #Pega os produtos mais vendidos
            for j in orders_sorted:
                
                #Pega os nomes dos produtos
                nome_prods = Produto.objects.get(id=j['id_produto'])

                #Novo obj com os nome e as quantidades
                name_and_quantity = {
                    'nome': nome_prods.nome,
                    'quantidade': j['c']
                }

                all_products_order.append(name_and_quantity)
        else:
            all_products_order = False
            
    else:
        info_produtos = None

    print(all_products_order)

    return render(
        request,
        'dashboard.html',
        {
            'range': range(9),
            'info': info_restaurante,
            'ult_produtos': info_produtos,
            'vendas': vendas,
            'lucro': lucro,''
            'ultimas_vendas': ultimas_vendas,
            'todos_produtos': all_products_order,
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

    if request.method == 'POST' and request.is_ajax():

        email = request.POST['email']
        senha = request.POST['senha']

        #Pesquisa o email na tabela de usuário
        try:
            usuario = User.objects.filter(email=email)
        except User.DoesNotExist:
            usuario = None

        #Se o usuaio não existir retorna erro
        if not usuario:
            return JsonResponse({ 'status': 'error' , 'msg': 'Esse email não está cadastrado :('})

        print(usuario)

        if usuario.exists():
            for i in usuario:
                user = auth.authenticate(username=i, password=senha)
        else:
            user = None

        if user is not None:
            auth.login(request, user)
            return JsonResponse({ 'status': 'success' , 'msg': 'Bem vindo ao nosso sistema'})
            # return redirect('/')
        else:
            return JsonResponse({ 'status': 'error' , 'msg': 'Verifique os dados inseridos :('})

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

    teste = []

    mais_produtos = Produto.objects.filter(restaurante_id=produto.restaurante.id)[:2]

    #Pega os comentarios
    try:
        comentarios = Comentario.objects.filter(produto_id=produto.id)
    except Comentario.DoesNotExist:
        comentarios = False

    if comentarios is not None:
        for i in comentarios:
            teste.append(5 - int(i.nota))
    else:
        teste = 0

    print(teste)

    return render(
        request,
        'produto_info.html',
        {
            'nota': str(produto.nota),
            'produto': produto,
            'mais_produtos': mais_produtos,
            'comentarios': comentarios,
            'teste': teste
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
    favoritos = None
    coment = None
    orders_finais = []
    orders_num = []

    #Redireciona o user que não estiver logado
    if not request.user.is_authenticated:
        return redirect('/login')

    #Redireciona o user que é dono de restaurante
    if request.user.groups.filter(name="Donos").exists():
        return redirect('/dashboard')

    #Pega instancia do cliente
    try:
        cliente = Cliente.objects.get(user_id=id)
        success = True

    except Cliente.DoesNotExist:
        msg = 'Erro ao encontrar o cliente'

    #Pega as orders do cliente
    try:
        #Número dos pedidos que o cliente fez
        orders_1 = Order.objects.filter(id_cliente=cliente.id)

        #Produtos relacionados com o cliente 
        orders_item = Placed_order.objects.filter(id_cliente=cliente.id)
        orders = list(set(orders_1))

        if not orders:
            msg = 'Nenhum pedido encontrado'

    except Placed_order.DoesNotExist:
        orders = None
        msg = 'Nenhum pedido encontrado'
        orders_item = None

    #Pega os status da compra
    try:
        status = Status.objects.all()
    except Status.DoesNotExist:
        status = None


    #Cadastro
    #Pegar dados existentes
    try:
        #Pega os dados do cliente para por no Form
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

        #Cria instancia do form de endereço
        add_endereco = AddAddress(request.POST or None)

    except Cliente.DoesNotExist:
        form = MoreInfoCliente(request.POST or None, request.FILES or None)
        add_endereco = AddAddress(request.POST or None)

    #Salvar os dados
    if request.method == 'POST':
        if form.is_valid():
            form.save()

    #Procura o endereço
    try:
        cl= Cliente.objects.filter(user_id=id)

        for i in cl:
            enderecos = Endereco.objects.filter(id_cliente=i.id)
    except:
        enderecos = False

    #Pega os favoritos
    try:
        cliente_fav = Cliente.objects.get(user_id=id)
        favoritos = Favoritos.objects.filter(id_cliente=cliente_fav.id)
    except Favoritos.DoesNotExist:
        favoritos = None

    #Pega os comentarios
    try:
        coment = Comentario.objects.filter(cliente_id=cliente[0].id)
    except Comentario.DoesNotExist:
        coment = None

    return render(
        request,
        'minha_conta.html',
        {
            "id": id,
            "cliente": cliente,
            'msg': msg,
            'pedidos': orders_item,
            'orders': orders,
            'add_endereco': add_endereco,
            'form': form,
            'favoritos': favoritos,
            'status': status,
            'coment': coment,
            'enderecos': enderecos,
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

def remover_produtos(request):
    if request.method == 'POST' and request.is_ajax():

        id = request.POST['id']

        try:
            prod = Produto.objects.get(id=id)

            prod.delete()

            msg = 'Produto #{} removido'.format(id)
            return JsonResponse({ 'status': 'success', 'msg': msg})

        except Produto.DoesNotExist:
            msg = 'Erro ao deletar o produto #{}'.format(id)
            return JsonResponse({ 'status': 'error', 'msg': msg})

def produtos_todos(request):
    rest = Restaurante.objects.get(user_id=request.user.id)
    produtos = list(Produto.objects.filter(restaurante_id = rest.id).values())

    data = dict()
    data['produtos'] = produtos
    print(produtos)

    return JsonResponse(data)

def produtos_editar(request, id):

    prod = Restaurante.objects.get(id=id)

    produtos = list(Produto.objects.filter(restaurante_id = rest.id).values())

    data = dict()
    data['produtos'] = produtos
    print(produtos)

    return JsonResponse(data)

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
            is_item = Carrinho.objects.get(id_produto=id_produto, id_cliente=id_user)
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
        success = False
        preco_carrinho = 0
        item = None
        taxa_entrega = 0
        msg_entrega = []
        final = 0

    if request.user.groups.filter(name="Donos").exists():
        msg = 'Você tem que ser cliente para ver os items no carrinho'
        success = False
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
        success = False

    if id_user is not None:
        try:
            item = Carrinho.objects.filter(id_cliente=id_user, is_carrinho=1)

            if item:
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
            
            else:
                msg = 'Esse usuário não possui nenhum item em seu carrinho'
                success = False
                preco_carrinho = 0
                taxa_entrega = 0
                msg_entrega = []
                final = 0

        except Carrinho.DoesNotExist:
            item = None
            success = False
            msg = 'Nenhum item no carrinho'
            preco_carrinho = 0
            taxa_entrega = 0
            msg_entrega = []
            final = 0

            return redirect('/login')

    print(item)

    
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
            already_exists = Favoritos.objects.get(id_produto=id_produto,id_cliente=id_user.id)
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
            print(id_produto)
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
            already_exists = Favoritos.objects.get(id_produto=id_produto,id_cliente=id_user.id)
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
    success = False
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
    if id_user is not None:
        try:
            items = Carrinho.objects.filter(id_cliente=id_user.id)
            
            if items:
                success = True
                msg = None

                for index,i in enumerate(items, start=1):
                    if index >= 1 and i.id_produto.restaurante.nome != i.id_produto.restaurante.nome:
                        taxa_entrega += i.id_produto.restaurante.taxa_entrega
                    else:
                        taxa_entrega = i.id_produto.restaurante.taxa_entrega

                    total += (i.id_produto.preco * i.quantidade)
            
                final = total + taxa_entrega

            else:
                success = False
                msg = 'Faça compras antes de prosseguir ao checkout'

        except Carrinho.DoesNotExist:
            items = None

        if id_user.endereco_id is None :
            tem_endereco = False
        else:
            tem_endereco = True

        try:
            main_address = Endereco.objects.get(id_cliente=id_user.id, is_principal=1)
        except Endereco.DoesNotExist:
            main_address = False

    else:
        tem_endereco = False
        
    return render(
        request,
        'checkout.html',
        {
            'items': items,
            'success': success,
            'msg': msg,
            'total': total,
            'taxa_entrega': taxa_entrega,
            'final': final,
            'usuario': id_user,
            'tem_endereco': tem_endereco,
            'main_address': main_address
        }
    )

def confirma(request):
    
    if request.method == 'POST' and request.is_ajax():

        #Variaveis de retorno
        cliente = None
        items_carrinho = None

        #Verifica se user está logado
        if not request.user.is_authenticated:
            redirect('/')

        #Pega dados do cliente que está comprando
        try:
            cliente = Cliente.objects.get(user_id=request.user.id)
        except Cliente.DoesNotExist:
            cliente = None

        #Pega produtos da compra
        if cliente is not None:
            try:
                items_carrinho = Carrinho.objects.filter(id_cliente=cliente.id)

                #Cria uma order
                order = Order(id_cliente=cliente)

                #Salva order
                order.save()

                #pega o ultimo id
                ultimo_id = Order.objects.latest('id')

                #Verifica se order ja existe
                try:
                    order_exist = Placed_order.objects.filter(order_id=ultimo_id.id).exists()
                except Placed_order.DoesNotExist:
                    order_exist = True
        
                if not order_exist:
                    #Salva os produtos como compra
                    for it in items_carrinho:
                        #Instancia do Restaurante
                        rest = Restaurante.objects.get(id=it.id_produto.restaurante.id)
                        
                        #Cria um pedido
                        item_order = Placed_order(endereco_entrega=cliente.endereco_id.endereco,
                                            endereco_saida=it.id_produto.restaurante.endereco,
                                            id_cliente=it.id_cliente,
                                            id_restaurante=rest,
                                            id_produto=it.id_produto,
                                            quantidade=it.quantidade,
                                            order_id=ultimo_id)

                        #Salva os pedidos        
                        item_order.save()

                        #limpa Carrinho
                        limpa_carrinho = Carrinho.objects.filter(id_produto=it.id_produto)

                        #Remove do Carrinho
                        limpa_carrinho.delete()
                    
                        #Mandar notificação ao restaurante
                        #Pega instancia do user
                        rest_user = Restaurante.objects.get(id=it.id_produto.restaurante.id)

                        n_aguento_mais = User.objects.get(id=rest_user.user_id)

                        msg = 'Atenção, o usuário #{} acaba de comprar {} unidade(s) do produto {}. Finalizando em um total de R${}'.format(it.id_cliente.user_id, it.quantidade, it.id_produto.nome, (it.id_produto.preco * it.quantidade) )
                        notificacao = Notificacao(mensagem=msg,
                                                id_user=n_aguento_mais)

                        notificacao.save()
                
                try:
                    has_status = Status.objects.filter(id_compra=ultimo_id.id).exists()
                except Status.DoesNotExist:
                    has_status = False

                #Salva compra com status
                if not has_status:

                    #Pega instacia
                    new_order = Order.objects.get(id=ultimo_id.id)

                    new_status = Status(recebido=1,id_compra=new_order)

                    new_status.save()

                    # for i in new_order:
                    #     #Cria instancia do Status
                    #     new_status = Status(recebido=1,id_compra=i)

                    #     #Salva status
                    #     new_status.save()

                else:
                    return HttpResponse('Ja tem essa order')

                msg = 'Obrigado pela compra :)'
                return JsonResponse({ 'status': 'success', 'msg': msg })

            except Carrinho.DoesNotExist:
                items_carrinho = None
                msg = 'Ops, Algo de errado não está certo :('
                return JsonResponse({ 'status': 'error', 'msg': msg })

        else:
            redirect('/login')

    else:
        redirect('/')

def dashboard_vendas(request):

    #Verifica se user está logado
    if not request.user.is_authenticated:
        redirect('/')

    vendas = False
    vendas_unique = False
    status = []

    try:
        id_user = Restaurante.objects.get(user_id=request.user.id)
    except Restaurante.DoesNotExist:
        id_user = None

    if id_user is not None:

        #Pega todas as vendas do restaurante
        try:
            vendas = Placed_order.objects.filter(id_restaurante=id_user.id).order_by('-id')
        except Placed_order.DoesNotExist:
            vendas = False

    else:
        redirect('/login')

    if vendas:
        vendas_unique = []

        for i in vendas:
            if i.order_id.id not in vendas_unique:
                vendas_unique.append(i.order_id.id)

        status = []

        for j in vendas_unique:
            stat = Status.objects.filter(id_compra=j)
            
            for k in stat:
                status.append(k)

    return render(
        request,
        'dashboard_vendas.html',
        {
            'vendas': vendas,
            'todas_vendas': vendas_unique,
            'status': status,
        }
    )

def get_status(request):

    #Verifica se é AJAX
    if request.method == 'GET' and request.is_ajax():

        #Verifica se user está logado
        if not request.user.is_authenticated:
            redirect('/')

        #Pega o id que ta vindo
        id_compra = request.GET['id']

        status_atual = 'ops..'
    
        #Pega no status
        try:
            status = Status.objects.get(id_compra=id_compra)

            if status.recebido:
                status_atual = 'recebido'
            elif status.saiu:
                status_atual = 'saiu'
            elif status.em_rota:
               status_atual = 'em_rota'
            elif status.entregue:
                status_atual = 'entregue'

            titulo = 'Status do pedido {}'.format(status.id_compra.id)
            return JsonResponse({ 'status': 'success' , 'titulo': titulo , 'atual': status_atual})


        except Status.DoesNotExist:
            msg: 'Não foi possivel encontrar essa compra'
            return JsonResponse({ 'status': 'error' , 'msg': msg})

    return JsonResponse({ 'status': 'error' , 'msg': 'Request Inválido'})

def editar_status(request):

    #Verifica se é AJAX
    if request.method == 'POST' and request.is_ajax():

        #Verifica se user está logado
        if not request.user.is_authenticated:
            redirect('/')

        #Pega o id que ta vindo
        id_compra = request.POST['id']
        tipo = request.POST['data'].replace('select=', '')

        status_atual = 'ops..'
    
        #Pega no status
        try:
            status = Status.objects.get(id_compra=id_compra)
            
            #Zera todos
            status.recebido = 0
            status.saiu = 0
            status.em_rota = 0
            status.entregue = 0

            if tipo == 'recebido':
                status.recebido = 1
            elif tipo == 'saiu':
                status.saiu = 1
            elif tipo == 'em_rota':
                status.em_rota = 1
            elif tipo == 'entregue':
                status.entregue = 1

            status.save()

            #Manda notificação para o dono

            if request.user.id is not None:
                try:
                    msg_not = "Uau, o status do pedido {} foi alterado para '{}'".format(id_compra, tipo)
                    notif = Notificacao(mensagem=msg_not, id_user=request.user)

                    notif.save()
                except Notificacao.DoesNotExist:
                    notif = ''

            msg = 'O pedido {} foi alterado para {}'.format(id_compra, tipo)
            return JsonResponse({ 'status': 'success' , 'msg': msg, 'tipo': tipo})

        except Status.DoesNotExist:
            msg: 'Não foi possivel encontrar essa compra'
            return JsonResponse({ 'status': 'error' , 'msg': msg})

    return JsonResponse({ 'status': 'error' , 'msg': 'Request Inválido'})

def comentario_adicionar(request):
    #Verifica se é AJAX
    if request.method == 'POST' and request.is_ajax():
        #Verifica se user está logado
        if not request.user.is_authenticated:
            redirect('/')
        
        #Pega as variaveis
        descricao       = request.POST['descricao']
        nota            = request.POST['nota']
        recomenda       = request.POST['recomenda']
        cliente_id      = request.POST['cliente_id']
        produto_id      = request.POST['produto_id']
        restaurante_id  = request.POST['restaurante_id']

        #Cria as instancias
        try:
            cliente = Cliente.objects.get(user_id=cliente_id)
        except Cliente.DoesNotExist:
            cliente = None

        try:
            produto = Produto.objects.get(id=produto_id)
        except produto.DoesNotExist:
            produto = None

        try:
            restaurante = Restaurante.objects.get(id=restaurante_id)
        except Restaurante.DoesNotExist:
            restaurante = None

        if cliente is not None and produto is not None and restaurante is not None:
            comentario = Comentario(nota=nota, descricao=descricao,cliente_id=cliente, produto_id=produto, restaurante_id=restaurante)

            comentario.save()

            msg = "Pronto \o/, você deixou um comentário nesse produto"
            return JsonResponse({ 'status': 'success' , 'msg': msg})
        
        else:
            return JsonResponse({ 'status': 'error' , 'msg': 'Ocorreu um erro'})

    return JsonResponse({ 'status': 'error' , 'msg': 'Request Inválido'})

def ajuda(request):

    total = Produto.objects.all().count()

    return render(
        request,
        'ajuda.html',
        {
            'total': total
        }
    )

def faq(request):
    return render(
        request,
        'faq.html',
    )

def dashboard_relatorio(request):

    return render(
        request,
        'dashboard_relatorio.html'
    )

def relatorio_vendas(request):

    data = []
    total = 0

    #Verifica se é AJAX
    if request.method == 'GET' and request.is_ajax():

        #Verifica se user está logado
        if not request.user.is_authenticated:
            redirect('/')

        id = request.GET['id']

        #Pega a instancia do restaurante
        try:
            restaurante = Restaurante.objects.get(user_id=id)
        except Restaurante.DoesNotExist:
            restaurante = False

        if restaurante:
            
            try:
                orders = Placed_order.objects.filter(id_restaurante=restaurante.id)
            except Placed_order.DoesNotExist:
                orders = None

            if orders is not None:

                for i in orders:

                    total += (i.id_produto.preco * i.quantidade)

                    all_orders = {
                        'id': i.id,
                        'time': formats.date_format(i.order_time, format='d/m/y'),
                        'cliente': i.id_cliente.id,
                        'produto': i.id_produto.nome,
                        'quantidade': i.quantidade,
                        'total': total,
                    }

                    data.append(all_orders)

                    total = 0

                return JsonResponse({'status':'success', 'data': data}, safe=False)

        return JsonResponse({'status':'error', 'msg': 'Você ainda não possui nenhuma compra para solicitar os relatórios'})



    return JsonResponse({ 'status': 'error' , 'msg': 'Request Inválido'})


def relatorio_produtos(request):

    data = []

    #Verifica se é AJAX
    if request.method == 'GET' and request.is_ajax():

        #Verifica se user está logado
        if not request.user.is_authenticated:
            redirect('/')

        id = request.GET['id']

        #Pega a instancia do restaurante
        try:
            restaurante = Restaurante.objects.get(user_id=id)
        except Restaurante.DoesNotExist:
            restaurante = False

        if restaurante:
            
            try:
                produtos = Produto.objects.filter(restaurante_id=restaurante.id)
            except Produto.DoesNotExist:
                produtos = None

            if produtos is not None:

                for i in produtos:

                    all_produtos = {
                        'id': i.id,
                        'nome': i.nome,
                        'descrição': i.descricao,
                        'preco': i.preco,
                        'categoria': i.categoria,
                        'nota': i.nota,
                    }

                    data.append(all_produtos)

                return JsonResponse({'status':'success', 'data': data}, safe=False)

        return JsonResponse({'status':'error', 'msg': 'Você ainda não possui nenhum produto para solicitar os relatórios'})



    return JsonResponse({ 'status': 'error' , 'msg': 'Request Inválido'})

    
def relatorio_financeiro(request):

    #Verifica se é AJAX
    if request.method == 'GET' and request.is_ajax():

        #Verifica se user está logado
        if not request.user.is_authenticated:
            redirect('/')

        id = request.GET['id'] 
        
        return JsonResponse({'status':'success', 'msg': 'Em manutenção!'})



    return JsonResponse({ 'status': 'error' , 'msg': 'Request Inválido'})

def finaliza(request):

    if not request.user.is_authenticated:
        return redirect('/')

    return render(
        request,
        'finaliza.html',
    )

def make_principal(request):

    id = request.POST['id']

    #Verifica se é ajax
    if request.method == 'POST' and request.is_ajax():

        #Pega instancia do Cliente
        try:
            cliente = Cliente.objects.get(user_id=request.user.id)
        except Cliente.DoesNotExist:
            cliente = None

        #Pega instancia do endereço
        if cliente is not None:
            try:
                endereco = Endereco.objects.filter(id_cliente=cliente.id)
            except Endereco.DoesNotExist:
                endereco = None
        else:
            endereco = None

        #Transforma todos os endereçoes em não principais
        if endereco is not None:
            
            for e in endereco:
                e.is_principal = False

                e.save()

            #Transforma um único em principal
            try:
                main = Endereco.objects.get(id=id)
            except Endereco.DoesNotExist:
                main = False

            if main:
                main.is_principal = True

                main.save()

                return JsonResponse({ 'status': 'success' , 'msg': 'Endereço principal alterado :)'})
            else:
                return JsonResponse({ 'status': 'error' , 'msg': 'Houve um erro ao realizar a ação :('})

        else:
            return JsonResponse({ 'status': 'error' , 'msg': 'Houve um erro ao realizar a ação :('})

    else:
        return JsonResponse({ 'status': 'error' , 'msg': 'Request Inválido'})

def add_endereco(request):
    
    user = request.user.id

    #Verifica se é ajax
    if request.method == 'POST':

        form = AddAddress(request.POST)

        if form.is_valid():

            try:
                cli = Cliente.objects.get(user_id=user)
            except Cliente.DoesNotExist:
                cli = None

            if cli is not None:
                ende = form.save(commit=False)

                ende.id_cliente = cli
                ende.save()

            return redirect('/conta/{}'.format(request.user.id))
        else:
            print(form.errors)
            return redirect('/conta/{}'.format(request.user.id))

    else:
        return JsonResponse({ 'status': 'error' , 'msg': 'Request Inválido'})