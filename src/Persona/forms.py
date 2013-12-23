from django.forms import ModelForm


from Persona.models import Persona

class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre','apellido', 'correo', 'dirpostal', 'institucion', 'telefono', 'pais', 'pagina']
        
class CorreoForm(forms.Form):
    correo = forms.EmailField()

