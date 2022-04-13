from django.db import models
from postagens.models import Postagem
from django import forms
# Create your models here.

class FormPostagem(forms.ModelForm):
    class Meta:
        model = Postagem
        exclude = ('data_postagem', 'postado')