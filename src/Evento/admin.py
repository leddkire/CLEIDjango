from django.contrib import admin
from Evento.models import Apertura
from Evento.models import Clausura
from Evento.models import EventoSocial
from Evento.models import Ponencia
from Evento.models import CharlaInvitada
from Evento.models import Taller

admin.site.register(Apertura)
admin.site.register(Clausura)
admin.site.register(EventoSocial)
admin.site.register(Ponencia)
admin.site.register(CharlaInvitada)
admin.site.register(Taller)