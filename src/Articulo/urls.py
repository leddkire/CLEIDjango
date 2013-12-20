from django.conf.urls import patterns, url

#Uncomment the next two lines to enable the admin:
from Articulo import views

urlpatterns = patterns('',
    # /articulo/
    url(r'^$', views.indice, name='indice'),
    #/articulo/mostrarFormArticulo/
    url(r'^mostrarFormArticulo/$', views.mostrarFormArticulo, name='mostrarFormArticulo'),
    #/articulo/crear/
    url(r'^crear/$', views.crear, name='crear'),
    #/articulo/<articulo_id>
    url(r'^(?P<articulo_id>\d+)/$', views.detalle, name='detalle')
)
