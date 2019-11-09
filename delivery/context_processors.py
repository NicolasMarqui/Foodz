from .models import Notificacao, Restaurante
from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2

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

# def cliente_ip(request):
#     client_ip = get_client_ip(request)
#     g = GeoIP2()

#     if client_ip is None:
#         city = 'Indaiatuba'
#     else:
#         # We got the client's IP address
#         city = client_ip
#         ip = request.META.get('REMOTE_ADDR', None)

#         if ip != '127.0.0.1 ':
#             city =  g.city(client_ip[0])
#         else:
#             city = 'Indaiatuba'
    

#     print(city)

#     return{
#         'city': city
#     }