from django.forms import ModelForm
from Evento.models import Evento, Apertura, Clausura, Taller, Ponencia, CharlaInvitada, EventoSocial

class EventoForm(ModelForm):
    class Meta:
        model = Evento
        fields = ['lugar','titulo', 'duracion', 'fechaIni', 'horaIni']
        

class EventoFormParaLugar(ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'duracion', 'fechaIni', 'horaIni']