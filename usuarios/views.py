from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import FormPostagem
# Create your views here.
def login(request):
    if request.method != 'POST':
        return render(request, 'login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.add_message(request, messages.ERROR, f'ERRO! Usuário ou senha inválidos')
        return render(request, 'login.html')
    else:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, f'Login feito com sucesso!')
        return redirect('colaborador')
        

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'cadastro.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.add_message(request, messages.ERROR, 'ERRO! nenhum campo pode ficar vazio')
        return render(request, 'cadastro.html')
    
    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'ERRO! senhas não conferem')
        return render(request, 'cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.ERROR, f'ERRO! Usuário {usuario} já existe')
        return render(request, 'cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, f'ERRO! Email {email} já existe')
        return render(request, 'cadastro.html')
    else:
        user = User.objects.create_user(username=usuario, email=email,  password=senha, first_name=nome, last_name=sobrenome)
        user.save()
        messages.add_message(request, messages.SUCCESS, f'Cadastro de {usuario} feito com sucesso, faça seu login')
        return redirect('login')
    
@login_required(login_url='/usuarios/login')
def index_colaborador(request):
    return render(request, 'colaborador.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url='/usuarios/login')
def artigo(request):
    if request.method != 'POST':
        form = FormPostagem()
        return render(request, 'artigo.html', {'form':form})
    form = FormPostagem(request.POST, request.FILES)
    if not form.is_valid():
        messages.add_message(request, messages.ERROR, 'Erro no formulário')
        return render(request, 'artigo.html', {'form':form})
    
    else:
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Post publicado com sucesso')
        return redirect('colaborador')
    



