from django.conf.urls import patterns, url

from Evento import views

urlpatterns = patterns('',
    # /evento/
    url(r'^$', views.indice, name='indice'),
    # /evento/evento_id/
    url(r'^(?P<evento_id>\d+)/(?P<evento_tipo>\w+)/$', views.detalle, name='detalle'),
    # /evento/definirEvento/
    url (r'^definirEvento/$', views.definirEvento, name ='definirEvento'),
    # /lugar/mostrarForm<evento_tipo>
    url(r'^mostrarForm(?P<evento_tipo>\w+)/$', views.mostrarFormEvento, name='mostrarFormEvento'),
    # /evento/crear<evento_tipo>/
    url (r'^crear(?P<evento_tipo>\w+)/$', views.crear, name = 'crear'),
)

