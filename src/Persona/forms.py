from django.forms import ModelForm
from Persona.models import Persona, Participante

class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre','apellido', 'correo', 'dirpostal', 'institucion', 'telefono', 'pais', 'pagina']
