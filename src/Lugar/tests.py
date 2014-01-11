from django.test import TestCase
from Lugar.models import Lugar

class LugarTestCase(TestCase):
    def test_lugar(self):
        l = Lugar(nombre = "Caracas", ubicacion = "Mys 213", capacidadMax = 30)
        self.assertEqual(l.nombre, "Caracas")
        self.assertEqual(l.ubicacion, "Mys 213")
        self.assertEqual(l.capacidadMax, 30)
        
    def test_lugarVista(self):
        l = Lugar(nombre = "Caracas", ubicacion = "Mys 213", capacidadMax = 30)
        l.save()
        resp = self.client.get('/lugar/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('listaLugares' in resp.context)
        self.assertEqual(len(resp.context['listaLugares']),1)
        lugar_1 = resp.context['listaLugares'][0]
        self.assertEqual(lugar_1.nombre, "Caracas")
        self.assertEqual(lugar_1.ubicacion, "Mys 213")
        self.assertEqual(lugar_1.capacidadMax, 30)
