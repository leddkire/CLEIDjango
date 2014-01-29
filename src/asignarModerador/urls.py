from django.conf.urls import patterns, url

from asignarModerador import views

urlpatterns = patterns('',                       
        #/asignarModerador/
        url(r'^$', views.indice, name='indice'),
        #/asignarModerador/mostrarMods/evento_tipo/evento_id/
        url(r'^mostrarMods/(?P<evento_tipo>\w+)/(?P<evento_id>\d+)/$', views.mostrarMods, name='mostrarMods'),
        #/asignarModerador/evento_tipo/evento_id/
        url(r'^(?P<evento_tipo>\w+)/(?P<evento_id>\d+)/$', views.asignarMod, name='asignarMod'),
        


)