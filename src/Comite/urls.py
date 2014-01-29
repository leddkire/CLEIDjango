from django.conf.urls import patterns, url

from Comite import views
from Persona.models import Persona

urlpatterns = patterns('',
    # /comite/
    url(r'^$', views.indice, name='indice'),
    url(r'^(?P<comite_correo>[^@]+@[^@]+\.[^@]+)/$', views.detalle, name='detalle'),
    url(r'^mostrarFormComprobar/$',views.mostrarFormComprobar, name='mostrarFormComprobar'),
    url(r'^comprobarEmailComite/$',views.comprobarEmailComite, name='comprobarEmailComite'),
    url(r'^crearComite/$', views.crearComite, name='crearComite'),
    url(r'^agregarMod/$',views.agregarMod, name = 'agregarMod'),
    
)
