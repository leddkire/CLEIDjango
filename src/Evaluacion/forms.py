from django.forms import ModelForm
from Evaluacion.models import Evaluacion,Nota

class EvaluacionForm(ModelForm):
    class Meta:
        model = Nota
        fields = ['valor']
        
