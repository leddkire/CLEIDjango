from django.conf.urls import patterns, url

from Conferencia import views

urlpatterns = patterns('',

    url(r'^$', views.indice, name='indice'),
    
    url(r'^mostrarFormConferencia/$',views.mostrarFormConferencia, name='mostrarFormConferencia'),
    url(r'^editarDatosConferencia/$', views.editarDatosConferencia, name='editarDatosConferencia'),
    url(r'^mostrarTiposDeArticulos/$', views.mostrarTiposDeArticulos, name='mostrarTiposDeArticulos'),
    url(r'^aceptablesNota/$', views.aceptablesNota, name='aceptablesNota'),
    #url(r'^comprobarEmailComite/$',views.comprobarEmailComite, name='comprobarEmailComite'), 
)
