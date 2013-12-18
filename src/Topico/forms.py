from django.forms import ModelForm
from Topico.models import Topico

class TopicoForm(ModelForm):
    class Meta:
        model = Topico
        fields = ['nombre']