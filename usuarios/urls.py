from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('colaborador/', views.index_colaborador, name='colaborador'),
    path('logout/', views.logout, name='logout'),
    path('colaborador/artigo/', views.artigo, name='artigo'),
    path('colaborador/lista/<int:id_autor>', views.listar_posts, name='lista'),
    path('colaborador/alterar/<int:id>', views.alterar_postagem, name='alterar'),
    
]