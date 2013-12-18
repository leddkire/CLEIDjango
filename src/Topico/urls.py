from django.conf.urls import patterns, url

from Topico import views

urlpatterns = patterns('',
    # /topico/
    url(r'^$', views.indice, name='indice'),
    # /topico/crearTopico/
    url(r'^crearTopico/$', views.crearTopico, name='crearTopico'),
    
    url(r'^mostrarFormTopico$',views.mostrarFormTopico, name='mostrarFormTopico')
)
