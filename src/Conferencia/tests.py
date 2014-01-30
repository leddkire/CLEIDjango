from django.test import TestCase
from Conferencia.models import Conferencia

class ConferenciaTestCase(TestCase):
    def test_conferencia(self):
        c = Conferencia(anio = 2013, duracion = 2, pais = "Venezuela", maxArticulos = 100)
        self.assertEqual(c.anio, 2013)
        self.assertEqual(c.duracion, 2)
        self.assertEqual(c.pais, "Venezuela")
        self.assertEqual(c.maxArticulos, 100)
        
    def test_conferenciaVista(self):
        
        conferencia_1 = Conferencia.objects.create(
                                                   anio = 2013,
                                                   duracion = 2,
                                                   pais = "Venezuela",
                                                   maxArticulos = 100
                                                   )
        resp = self.client.get('/conferencia/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('conferencia' in resp.context)
        self.assertEqual([conferencia.pk for conferencia in resp.context['conferencia']], [1])
        conferencia_1 = resp.context['conferencia'][0]
        self.assertEqual(conferencia_1.anio, 2013)
        self.assertEqual(conferencia_1.duracion, 2)
        self.assertEqual(conferencia_1.pais, "Venezuela")
        self.assertEqual(conferencia_1.maxArticulos, 100)
