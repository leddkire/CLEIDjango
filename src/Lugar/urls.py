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
    url(r'^opciones/(?P<lugar_id>\w+)/$', views.detalle, name='detalle'),
    # /lugar/lugar_id/asignarEvento
    url(r'^(?P<lugar_id>\w+)/definirEvento/$', views.definirEvento, name='definirEvento'),
    # /lugar/<lugar_id>/mostrarForm<evento_tipo>
    url(r'^(?P<lugar_id>\w+)/mostrarForm(?P<evento_tipo>\w+)/$', views.mostrarFormEvento, name='mostrarFormEvento'),
    # /lugar/lugar_id/asignar<evento_tipo>
    url(r'^(?P<lugar_id>\w+)/asignar(?P<evento_tipo>\w+)/$', views.asignar, name='asignar'),

)

