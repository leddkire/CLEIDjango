from django.conf.urls import patterns, url

from Evaluacion import views


urlpatterns = patterns('',
    # /evaluacion/
    url(r'^$', views.indice, name='indice'), 
    url(r'^detalle_(?P<clave>\d+)/$', views.detalle, name='detalle'),
    # /evaluacion/mostrarEvaluacion
    url(r'^mostrarEvaluacion/',views.mostrarFormEvaluacion,name='mostrarFormEvaluacion'),
    # /evaluacion/mostrarArbitro
    url(r'^mostrarArbitro/',views.mostrarArbitro,name='mostrarArbitro'),
    
    #url(r'^mostrarArticulo/',views.mostrarArticulo,name='mostrarArticulo'),
    
    url(r'^arbitro_(?P<arbitro_id>\d+)/$',views.mostrarArticulo,name='mostrarArticulo'),
    
    url(r'^arb_(?P<arbitro_id>\d+)/art_(?P<articulo_id>\d+)/$',views.mostrarFormEvaluar,name='mostrarFormEvaluar'),
    url(r'^(?P<arbitro>[^@]+@[^@]+\.[^@]+)/(?P<articulo>[0-9A-Za-z\s]+)$',views.crearEvaluacion,name='crearEvaluacion'),
   
    
)
