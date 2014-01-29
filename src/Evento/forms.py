from django.forms import ModelForm
from Evento.models import Evento, Apertura, Clausura, Taller, Ponencia, CharlaInvitada, EventoSocial

class EventoForm(ModelForm):
    class Meta:
        model = Evento
        fields = ['lugar','titulo', 'duracion', 'fechaIni', 'horaIni']

class TallerCharlaPonenciaForm(EventoForm):
    class Meta(EventoForm.Meta):
        model = Taller
        fields = EventoForm.Meta.fields + ['topico']

class EventoFormParaLugar(ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'duracion', 'fechaIni', 'horaIni']
        
class TallerCharlaPonenciaFormParaLugar(EventoFormParaLugar):
    class Meta(EventoFormParaLugar.Meta):
        model = Taller
        fields = EventoFormParaLugar.Meta.fields + ['topico']
        
