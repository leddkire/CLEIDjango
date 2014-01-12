from django.conf.urls import patterns, url

from Conferencia import views

urlpatterns = patterns('',

    url(r'^$', views.indice, name='indice'),
    
    url(r'^mostrarFormConferencia/$',views.mostrarFormConferencia, name='mostrarFormConferencia'),
    url(r'^editarDatosConferencia/$', views.editarDatosConferencia, name='editarDatosConferencia'),
    url(r'^mostrarTiposDeArticulos/$', views.mostrarTiposDeArticulos, name='mostrarTiposDeArticulos'),
    url(r'^aceptablesNota/$', views.aceptablesNota, name='aceptablesNota'),
    url(r'^comprobarPresidente/$', views.comprobarPresidente, name='comprobarPresidente'),
    url(r'^desempatar/$', views.desempatar, name='desempatar'),
    url(r'^reiniciarSeleccion/$', views.reiniciarSeleccion, name='reiniciarSeleccion'),
    url(r'^mostrarFormComprobar/$', views.mostrarFormComprobar, name='mostrarFormComprobar'),
    url(r'^(?P<articulo_id>\d+)/$', views.agregarAceptado, name='agregarAceptado'),
    url(r'^mostrarEstadoArticulos/$', views.mostrarEstadoArticulos, name='mostrarEstadoArticulos'),
    #url(r'^comprobarEmailComite/$',views.comprobarEmailComite, name='comprobarEmailComite'), 
)
