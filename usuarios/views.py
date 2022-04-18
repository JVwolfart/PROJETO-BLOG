from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from postagens.models import Categoria, Postagem
from django.core.paginator import Paginator
from django.utils import timezone



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

    if len(senha) < 6:
        messages.add_message(request, messages.ERROR, 'ERRO! senha deve ter mais de 6 caracteres')
        return render(request, 'cadastro.html')

    if len(senha) > 12:
        messages.add_message(request, messages.ERROR, 'ERRO! senha deve ter menos de 12 caracteres')
        return render(request, 'cadastro.html')

    if not senha.isalnum():
        messages.add_message(request, messages.ERROR, 'ERRO! senha não pode ter caracteres especiais, exemplo: (#@%$/*+-!&[}{]:;.), apenas alfanuméricos')
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

'''@login_required(login_url='/usuarios/login')
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
        messages.add_message(request, messages.SUCCESS, 'Post enviado com sucesso, será publicado logo após a revisão')
        return redirect('colaborador')'''


@login_required(login_url='/usuarios/login')
def artigo(request):
    categorias = Categoria.objects.all()
    if request.method != 'POST':
        return render(request, 'artigo2.html', {'categorias':categorias})
    titulo = request.POST.get('titulo').strip().title()
    resumo = request.POST.get('resumo').strip()
    conteudo = request.POST.get('conteudo').strip()
    categ = Categoria.objects.get(id=request.POST.get('categoria'))  
    foto = request.FILES.get('foto')
    autor = request.user
    
    postagem = Postagem.objects.create(titulo=titulo, resumo=resumo, conteudo=conteudo, categoria=categ, foto=foto, autor=autor)
    postagem.save()
    messages.add_message(request, messages.SUCCESS, 'Postagem enviada com sucesso, será publicado logo após a revisão.')
    return redirect('colaborador')
    

@login_required(login_url='/usuarios/login')
def listar_posts(request, id_autor):
    posts = Postagem.objects.all().order_by('-data_postagem').filter(
        autor=id_autor
    )
    paginator = Paginator(posts, 10)
    page = request.GET.get('p')
    posts = paginator.get_page(page)
    return render(request, 'lista_posts.html', {'posts': posts})

@login_required(login_url='/usuarios/login')
def listar_all_posts(request):
    posts = Postagem.objects.all().order_by('-data_postagem')
    paginator = Paginator(posts, 10)
    page = request.GET.get('p')
    posts = paginator.get_page(page)
    return render(request, 'lista_posts.html', {'posts': posts})

@login_required(login_url='/usuarios/login')
def alterar_postagem(request, id):
    
    postagem = Postagem.objects.get(id=id)

    if postagem.postado:
        postagem.postado = False

    form = FormPostagem(request.POST or None , request.FILES , instance=postagem)

    if request.method != 'POST':
        form = FormPostagem(request.POST or None, instance=postagem)
        return render(request, 'alterar.html', {'postagem':postagem, 'form':form})


    if not form.is_valid():
        form = FormPostagem(request.POST or None, instance=postagem)
        messages.add_message(request, messages.ERROR, 'Erro no formulário')
        return render(request, 'alterar.html', {'postagem':postagem, 'form':form})
    
    else:
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Post alterado com sucesso, será publicada logo após a revisão')
        return redirect('colaborador')


@login_required(login_url='/usuarios/login')
def autorizar_postagem(request, id):
    
    postagem = Postagem.objects.get(id=id)
    
    postagem.postado = True
    postagem.data_postagem = timezone.now()

    postagem.save()
    return redirect('lista_all')

@login_required(login_url='/usuarios/login')
def desligar_postagem(request, id):
    
    postagem = Postagem.objects.get(id=id)
    
    postagem.postado = False

    postagem.save()
    return redirect('lista_all')
