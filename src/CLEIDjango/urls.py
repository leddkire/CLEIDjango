from django.conf.urls import patterns, include, url

#Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^evento/', include('Evento.urls', namespace = "Evento")),
    url(r'^lugar/', include('Lugar.urls', namespace="Lugar")),
    url(r'^topico/', include('Topico.urls', namespace="Topico")),
    url(r'^articulo/', include('Articulo.urls', namespace="Articulo")),
    #url(r'^evaluacion/', include('Evaluacion.urls', namespace="Evaluacion")),
    # Examples:
    # url(r'^$', 'CLEIDjango.views.home', name='home'),
    # url(r'^CLEIDjango/', include('CLEIDjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
   
)
