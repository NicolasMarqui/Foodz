from .models import Notificacao, Restaurante

def notificacoes(request):

    notificacoes = Notificacao.objects.filter(id_user=request.user.id)

    return {
        'notificacoes': notificacoes,
    }

def profile_picture_owner(request):

    avatar = Restaurante.objects.get(user_id=request.user.id)

    return {
        'avatar': avatar.logo,
    }