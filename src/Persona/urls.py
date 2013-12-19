from django.conf.urls import patterns, url

from Persona import views

urlpatterns = patterns('',
    # /persona/
    url(r'^$', views.indice, name='indice'),
    # /persona/persona_id/
    url(r'^(?P<persona_id>\d+)/(?P<persona_tipo>\w+)/$', views.detalle, name='detalle'),
    # /persona/definirPersona/
    url (r'^definirPersona/$', views.definirPersona, name ='definirPersona'),
    # /lugar/mostrarForm<persona_tipo>
    url(r'^mostrarForm(?P<persona_tipo>\w+)/$', views.mostrarFormPersona, name='mostrarFormPersona'),
    # /persona/crear<persona_tipo>/
    url (r'^crear(?P<persona_tipo>\w+)/$', views.crear, name = 'crear'),
)
