from django.test import TestCase
from Topico.models import Topico

class TopicoTestCase(TestCase):
    def test_topico(self):
        t = Topico(nombre = "Ingenieria de Software")
        self.assertEqual(t.nombre, "Ingenieria de Software")
    
    def test_topicoVista(self):
        t = Topico(nombre = "Ingenieria de Software")
        t.save()
        resp = self.client.get('/topico/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('topicos' in resp.context)
        self.assertEqual([topico.pk for topico in resp.context['topicos']], ["Ingenieria de Software"])
        
    def test_topicoVistaForm(self):
        t = Topico(nombre = "Ingenieria de Software")
        t.save()
        resp = self.client.get('/topico/mostrarFormTopico')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        
