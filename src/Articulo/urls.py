from django.conf.urls import patterns, url

#Uncomment the next two lines to enable the admin:
from Articulo import views

urlpatterns = patterns('',
    # /articulo/
    url(r'^$', views.indice, name='indice'),
    
)
