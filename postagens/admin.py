from django.contrib import admin
from .models import Categoria, Postagem
# Register your models here.

class AdmCategoria(admin.ModelAdmin):
    list_display = ('id', 'categoria',)
    list_display_links = ('id', 'categoria',)
    list_per_page = 10
    search_field = ['categoria']

class AdmPostagem(admin.ModelAdmin):
    list_display = ('titulo', 'data_postagem', 'categoria', 'postado')
    list_display_links = ('titulo',)
    list_per_page = 10
    search_field = ['titulo', 'data_postagem']
    list_filter = ['categoria']
    list_editable = ('postado', )

admin.site.register(Categoria, AdmCategoria)
admin.site.register(Postagem, AdmPostagem)
