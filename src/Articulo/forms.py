from django.forms import ModelForm

from Articulo.models import Articulo

class ArticuloForm(ModelForm):
    class Meta:
        model = Articulo
        fields = ['titulo','palabrasClaves','resumen','texto'] 