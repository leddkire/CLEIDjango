from django.conf.urls import patterns, url

from Comite import views
from Persona.models import Persona

urlpatterns = patterns('',
    # /comite/
    url(r'^$', views.indice, name='indice'),
    # /comite/crearComite/
    url(r'^mostrarFormComprobar/$',views.mostrarFormComprobar, name='mostrarFormComprobar'),
    url(r'^comprobarEmailComite/$',views.comprobarEmailComite, name='comprobarEmailComite'),
    url(r'^crearComite/$', views.crearComite, name='crearComite'),
   
)
