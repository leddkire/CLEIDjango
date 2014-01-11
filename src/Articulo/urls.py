from django.conf.urls import patterns, url

#Uncomment the next two lines to enable the admin:
from Articulo import views

urlpatterns = patterns('',
    # /articulo/
    url(r'^$', views.indice, name='indice'),
    #/articulo/crear/articulo_id/Autor
    url(r'^crear/(?P<articulo_id>\d+)/Autor/$', views.crearAutor, name = 'crearAutor'),
    #/articulo/crear/articulo_id/Topico
    url(r'^crear/(?P<articulo_id>\d+)/Topico/$', views.crearTopico, name = 'crearTopico'),
    #/articulo/articulo_id/crearArticuloPasoAutor/
    url(r'^crear/ArticuloPasoAutor/$', views.crearArticuloPasoAutor, name='crearArticuloPasoAutor'),
    #/articulo/crearArticuloPasoDG/
    url(r'^crear/ArticuloPasoDG/$', views.crearArticuloPasoDG, name='crearArticuloPasoDG'),
    #/articulo/articulo_id/crearArticuloPasoTopico/
    url(r'^crear/(?P<articulo_id>\d+)/ArticuloPasoTopico/$', views.crearArticuloPasoTopico, name='crearArticuloPasoTopico'),
    #/articulo/comprobarEmail<articulo_id>/
    url(r'^revisarAutor(?P<articulo_id>\d+)/$',views.comprobarEmailAutor, name='revisarAutor'),
    #/articulo/<articulo_id>
    url(r'^(?P<articulo_id>\d+)/$', views.detalle, name='detalle')
)
