from django.conf.urls import patterns, url

from Inscripcion import views
from Persona.models import Persona


urlpatterns = patterns('',
    # /inscripcion/
    url(r'^$', views.indice, name='indice'),
    url(r'^(?P<inscripcion_correo>[^@]+@[^@]+\.[^@]+)/$', views.detalle, name='detalle'),
    # /inscripcion/mostrarFormComprobar
    url(r'^mostrarFormComprobar/$',views.mostrarFormComprobar, name='mostrarFormComprobar'),
    # /inscripcion/comprobarEmailInscripcion/
    url(r'^comprobarEmailInscripcion/$',views.comprobarEmailInscripcion, name='comprobarEmailInscripcion'),
    # /inscripcion/crearInscripcion/
    url(r'^crearInscripcion/$', views.crearInscripcion, name='crearInscripcion'),
)