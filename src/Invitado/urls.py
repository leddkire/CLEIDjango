from django.conf.urls import patterns, url

from Invitado import views

urlpatterns = patterns('',
    # /invitado/
    url(r'^$', views.indice, name='indice'),
    url(r'^(?P<invitado_correo>[^@]+@[^@]+\.[^@]+)/$', views.detalle, name='detalle'),
    url(r'^mostrarFormComprobar/$',views.mostrarFormComprobar, name='mostrarFormComprobar'),
    url(r'^comprobarEmailInvitado/$',views.comprobarEmailInvitado, name='comprobarEmailInvitado'),
    url(r'^crearInvitado/$', views.crearInvitado, name='crearInvitado'),
)