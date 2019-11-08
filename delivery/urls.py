from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('produtos/', views.produtos, name="Produtos"),
    path('dashboard/', views.dashboard, name="Dashboard"),
    path('dashboard/financeiro', views.dashboard_financeiro, name="Dashboard_financeiro"),
    path('dashboard/produtos', views.dashboard_produtos, name="Dashboard_produtos"),
    path('dashboard/config', views.dashboard_config, name="Dashboard_config"),
    path('sobre-nos', views.sobre_nos, name="Sobre Nós"),
    path('pesquisa/', views.pesquisa, name="pesquisa"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('produtos/info/<int:id>/', views.produto_info, name="Informação Produto"),
    path('restaurantes/', views.restaurantes, name="Restaurantes"),
    path('conta/<int:id>', views.minha_conta,name="Minha Conta"),
    path('logout',views.logout,name="logout"),
    path('lida',views.lida,name="Lida"),
    path('produtos/todos',views.produtos_todos,name="Todos os Produtos"),
    path('produtos/editar/<int:id>',views.produtos_editar,name="Editar produtos"),
    path('get-produto-editar',views.get_produto_editar,name="Editar Produto"),
    path('save-produto-editar',views.save_produto_editar,name="Editar Produto"),
]
