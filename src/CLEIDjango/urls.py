from django.conf.urls import patterns, include, url
from django.contrib import admin

#Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^evento/', include('Evento.urls', namespace = "Evento")),
    url(r'^lugar/', include('Lugar.urls', namespace="Lugar")),
    url(r'^topico/', include('Topico.urls', namespace="Topico")),
    url(r'^articulo/', include('Articulo.urls', namespace="Articulo")),
    url(r'^persona/', include('Persona.urls', namespace="Persona")),
    url(r'^comite/', include('Comite.urls', namespace="Comite")),
    url(r'^invitado/', include('Invitado.urls', namespace="Invitado")),
    url(r'^conferencia/', include('Conferencia.urls', namespace="Conferencia")),
    url(r'^evaluacion/', include('Evaluacion.urls', namespace="Evaluacion")),
    url(r'^inscripcion/', include('Inscripcion.urls', namespace = "Inscripcion")),

)

