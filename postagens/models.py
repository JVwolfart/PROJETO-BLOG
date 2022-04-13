from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    def __str__(self):
        return self.categoria

class Postagem(models.Model):
    titulo = models.CharField(max_length=100)
    data_postagem = models.DateTimeField(default=timezone.now)
    resumo = models.TextField()
    conteudo = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    foto = models.ImageField(blank=True, upload_to='fotos')
    postado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo