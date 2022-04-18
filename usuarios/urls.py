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
    path('colaborador/lista_all/', views.listar_all_posts, name='lista_all'),
    path('colaborador/alterar/<int:id>', views.alterar_postagem, name='alterar'),
    path('colaborador/autorizar/<int:id>', views.autorizar_postagem, name='autorizar'),
    path('colaborador/desligar/<int:id>', views.desligar_postagem, name='desligar'),
]