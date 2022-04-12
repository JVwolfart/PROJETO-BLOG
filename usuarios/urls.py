from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('colaborador/', views.index_colaborador, name='colaborador'),
    path('logout/', views.logout, name='logout'),
    path('colaborador/artigo/', views.artigo, name='artigo'),
]