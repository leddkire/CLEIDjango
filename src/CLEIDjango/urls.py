from django.conf.urls import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^persona/', include('Persona.urls', namespace = "Persona")),
    url(r'^inscripcion/', include('Inscripcion.urls', namespace = "Inscripcion")),
    # Examples:
    # url(r'^$', 'CLEIDjango.views.home', name='home'),
    # url(r'^CLEIDjango/', include('CLEIDjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)