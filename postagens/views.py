from itertools import count
from django.shortcuts import render, get_object_or_404
from .models import Categoria, Postagem
from django.core.paginator import Paginator
from django.db.models import Q, Count

# Create your views here.
def index(request):
    categorias = Categoria.objects.all().order_by('categoria')
    postagens = Postagem.objects.all().order_by('-id')
    postagem1 = Categoria.objects.order_by('categoria').annotate(n=Count('postagem'))
    
    paginator = Paginator(postagens, 4)
    page = request.GET.get('p')
    postagens = paginator.get_page(page)
    return render(request, 'index.html', {'postagens':postagens, 'postagem1':postagem1})

def busca(request):
    termo = request.GET.get('termo')
    categorias = Categoria.objects.all().order_by('categoria')
    postagens = Postagem.objects.filter(
        Q(titulo__icontains=termo) | Q(conteudo__icontains=termo)
    ).order_by('-id')
    postagem1 = Categoria.objects.order_by('categoria').annotate(n=Count('postagem'))
    paginator = Paginator(postagens, 4)
    page = request.GET.get('p')
    postagens = paginator.get_page(page)
    return render(request, 'pesquisa.html', {'postagens':postagens,  'postagem1':postagem1, 'termo':termo})

def busca_categoria(request, id):
    categorias = Categoria.objects.all().order_by('categoria')
    postagens = Postagem.objects.all().order_by('-id').filter(
        categoria = id
    )
    categoria = get_object_or_404(Categoria, id=id)
    postagem1 = Categoria.objects.order_by('categoria').annotate(n=Count('postagem'))
    paginator = Paginator(postagens, 4)
    page = request.GET.get('p')
    postagens = paginator.get_page(page)
    return render(request, 'categoria.html', {'postagens':postagens, 'categoria':categoria, 'postagem1':postagem1})


def postagem(request, id):
    postagem = get_object_or_404(Postagem, id=id)
    return render(request, 'postagem.html', {'postagem':postagem})

    