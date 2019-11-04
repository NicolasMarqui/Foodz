from .models import Notificacao, Restaurante

def notificacoes(request):

    notificacoes = Notificacao.objects.filter(id_user=request.user.id)

    return {
        'notificacoes': notificacoes,
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