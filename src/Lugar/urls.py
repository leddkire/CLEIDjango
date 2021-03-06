from django.conf.urls import patterns, url

from Lugar import views

urlpatterns = patterns('',
    # /lugar/
    url(r'^$', views.indice, name='index'),
    # /lugar/crear/
    url(r'^crear/$', views.crear, name='crear'),
    # /lugar/guardar
    url(r'^guardar/$', views.guardar, name='guardar'),
    # /lugar/lugar_id/
    url(r'^opciones/(?P<lugar_id>\d+)/$', views.detalle, name='detalle'),
    # /lugar/lugar_id/asignarEvento
    url(r'^(?P<lugar_id>\d+)/definirEvento/$', views.definirEvento, name='definirEvento'),
    # /lugar/<lugar_id>/mostrarForm<evento_tipo>
    url(r'^(?P<lugar_id>\d+)/mostrarForm(?P<evento_tipo>\w+)/$', views.mostrarFormEvento, name='mostrarFormEvento'),
    # /lugar/lugar_id/asignar<evento_tipo>
    url(r'^(?P<lugar_id>\d+)/asignar(?P<evento_tipo>\w+)/$', views.asignar, name='asignar'),

)

