from django.conf.urls import patterns, url

from Conferencia import views

urlpatterns = patterns('',

    url(r'^$', views.indice, name='indice'),
    
    url(r'^mostrarFormConferencia/$',views.mostrarFormConferencia, name='mostrarFormConferencia'),
    url(r'^editarDatosConferencia/$', views.editarDatosConferencia, name='editarDatosConferencia'),
    url(r'^mostrarTiposDeArticulos/$', views.mostrarTiposDeArticulos, name='mostrarTiposDeArticulos'),
    url(r'^aceptablesNota/$', views.aceptablesNota, name='aceptablesNota'),
    url(r'^comprobarPresidente/(?P<vista_sigue>\w+)/$', views.comprobarPresidente, name='comprobarPresidente'),
    url(r'^desempatar/$', views.desempatar, name='desempatar'),
    url(r'^reiniciarSeleccion/$', views.reiniciarSeleccion, name='reiniciarSeleccion'),
    url(r'^mostrarFormComprobar/(?P<vista_sigue>\w+)/$', views.mostrarFormComprobar, name='mostrarFormComprobar'),
    url(r'^agregarAceptado/(?P<articulo_id>\d+)/$', views.agregarAceptado, name='agregarAceptado'),
    url(r'^mostrarEstadoArticulos/$', views.mostrarEstadoArticulos, name='mostrarEstadoArticulos'),
    url(r'^elegirEspeciales/$', views.elegirEspeciales, name='elegirEspeciales'),
    url(r'^agregarEspecial/(?P<articulo_id>\d+)/$', views.agregarEspecial, name='agregarEspecial'),
    url(r'^llenarDiccionarioTopicos/$', views.llenarDiccionarioTopicos, name='llenarDiccionarioTopicos'),
    #url(r'^comprobarEmailComite/$',views.comprobarEmailComite, name='comprobarEmailComite'), 
)
