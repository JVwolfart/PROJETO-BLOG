from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('postagem/<int:id>', views.postagem, name='postagem'),
    path('busca/', views.busca, name='busca'),
    path('busca_categoria/<int:id>', views.busca_categoria, name='busca_categoria'),
]