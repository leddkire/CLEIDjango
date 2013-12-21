from django.conf.urls import patterns, url

from Invitado import views

urlpatterns = patterns('',
    # /comite/
    url(r'^$', views.indice, name='indice'),
    # /comite/crearComite/
    url(r'^mostrarFormComprobar/$',views.mostrarFormComprobar, name='mostrarFormComprobar'),
    url(r'^comprobarEmailInvitado/$',views.comprobarEmailInvitado, name='comprobarEmailInvitado'),
    url(r'^crearInvitado/$', views.crearInvitado, name='crearInvitado'),
)