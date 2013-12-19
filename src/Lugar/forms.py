from django.forms import ModelForm
from Lugar.models import Lugar

class LugarForm(ModelForm):
    class Meta:
        model = Lugar
        fields = ['nombre', 'ubicacion', 'capacidadMax']