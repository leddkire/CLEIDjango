from django.conf.urls import patterns, url

from Evento import views

urlpatterns = patterns('',
    # /evento/
    url(r'^$', views.indice, name='indice'),
    # /evento/evento_id/
    url(r'^(?P<evento_id>\d+)/(?P<evento_tipo>\w+)/$', views.detalle, name='detalle'),
)

