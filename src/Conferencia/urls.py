from django.conf.urls import patterns, url

from Conferencia import views

urlpatterns = patterns('',

    url(r'^$', views.indice, name='indice'),
    
    url(r'^mostrarFormConferencia/$',views.mostrarFormConferencia, name='mostrarFormConferencia'),
    url(r'^editarDatosConferencia/$', views.editarDatosConferencia, name='editarDatosConferencia'),
    #url(r'^comprobarEmailComite/$',views.comprobarEmailComite, name='comprobarEmailComite'), 
)
