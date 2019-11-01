from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('produtos/', views.produtos, name="Produtos"),
    path('dashboard/', views.dashboard, name="Dashboard"),
    path('sobre-nos', views.sobre_nos, name="Sobre Nós"),
    path('pesquisa/', views.pesquisa, name="pesquisa"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('produtos/info/<int:id>/', views.produto_info, name="Informação Produto"),
    path('restaurantes/', views.restaurantes, name="Restaurantes"),
    path('restaurantes/cadastro/', views.cadastro_restaurantes, name="Cadastro Restaurante"),
    path('conta/<int:id>', views.minha_conta,name="Minha Conta"),
    path('logout',views.logout,name="logout")
]
