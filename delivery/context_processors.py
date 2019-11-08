from .models import Notificacao, Restaurante

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