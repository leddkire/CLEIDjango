from django.forms import ModelForm
from Topico.models import Topico
from django import forms

class TopicoForm(forms.Form):
    nombre = forms.CharField(max_length=100)