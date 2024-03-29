from .models import Notificacao, Restaurante, Carrinho, Cliente, Placed_order

def notificacoes(request):

    notificacoes = Notificacao.objects.filter(id_user=request.user.id, foi_lida=0)

    todas_lidas = Notificacao.objects.filter(id_user=request.user.id, foi_lida=1)

    return {
        'notificacoes': notificacoes,
        'lidas': todas_lidas,
    }

def profile_picture_owner(request):

    have_finished = Restaurante.objects.filter(user_id = request.user.id)

    if '/dashboard' in request.path and have_finished:
        avatar = Restaurante.objects.get(user_id=request.user.id)

        return {
            'avatar': avatar.logo,
        }

    else:
        return {
            'Hello':  'Go to Dashboard to see profile'
        }


def quantidadeCarrinho(request):

    if not request.user.is_authenticated:
        return{
            'quantidade': 0
        }

    try:
        id_user = Cliente.objects.get(user_id=request.user.id)
    except Cliente.DoesNotExist:
        id_user = None

    try:
        quantidade = Carrinho.objects.filter(id_cliente=id_user, is_carrinho=1)

        return{
            'quantidade': quantidade.count()
        }
    except Carrinho.DoesNotExist:
        return{
            'quantidade': 0
        }

def precoCarrinho(request):
    if not request.user.is_authenticated:
        return{
            'preco': '%.2f' % 0,
            'hasItem': False
        }

    try:
        id_user = Cliente.objects.get(user_id=request.user.id)
    except Cliente.DoesNotExist:
        id_user = None

    try:
        preco = Carrinho.objects.filter(id_cliente=id_user, is_carrinho=1)
        total = 0

        for i in preco:
            total += (i.id_produto.preco * i.quantidade)

        return{
            'preco': total
        }
    except Carrinho.DoesNotExist:
        return{
            'preco': '%.2f' % 0,
            'hasItem': False
        }