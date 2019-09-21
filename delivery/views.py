from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(
        request,
        'index.html',
        {
            'range': range(9),
        }
    )

def produtos(request):
    return render(
        request,
        'produtos.html',
        {
            'range': range(9)
        }
    )

def dashboard(request):
    return render(
        request,
        'dashboard.html',
        {
            'range': range(9),
        }
    )

def financeiro(request):
    return render(
        request,
        'financeiro.html',
    )

def login(request):
    return render(
        request,
        'login.html',
    )

def produto_info(request,id = None):
    return render(
        request,
        'produto_info.html',
        {
            'range': range(5),
        }
    )