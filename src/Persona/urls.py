from django.conf.urls import patterns, url

from Persona import views

urlpatterns = patterns('',
    # /persona/
    url(r'^$', views.indice, name='indice'),
    # /lugar/mostrarForm<persona_tipo>
    url(r'^mostrarFormPersona/$', views.mostrarFormPersona, name='mostrarFormPersona'),
    # /persona/crear<persona_tipo>/
    url (r'^crear/$', views.crear, name = 'crear'),
)