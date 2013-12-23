from django.test import TestCase
from Persona.models import Persona
from Inscripcion.models import Inscripcion
from datetime import date
import unittest

# Create your tests here.

class Test(TestCase):

   def testInscripcion(self):
        p = Persona(correo = "patty@usb.ve", dirpostal = 1090)
        i = Inscripcion(correo = p, tarifa = 250, fechainscripcion = date(2013,12,24), fechatope = date(2013,12,31))
        self.assertEqual(p, i.correo)
        self.assertEqual(250, i.tarifa)
        self.assertEqual(date(2013,12,24), i.fechainscripcion)
        self.assertEqual(date(2013,12,31), i.fechatope)
        
   def test_InscripcionVista(self):
        p = Persona(correo = "patty@usb.ve", dirpostal = 1090)
        p.save()
        i = Inscripcion(correo = p, tarifa = 250, fechainscripcion = date(2013,12,24), fechatope = date(2013,12,31))
        i.save()
        resp = self.client.get('/inscripcion/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('inscripcion' in resp.context)
        self.assertEqual([inscripcion.pk for inscripcion in resp.context['inscripcion']], [1])
        inscripcion_1 = resp.context['inscripcion'][0]
        self.assertEqual(p, inscripcion_1.correo)
        self.assertEqual(250, inscripcion_1.tarifa)
        self.assertEqual(date(2013,12,24), inscripcion_1.fechainscripcion)
        self.assertEqual(date(2013,12,31), inscripcion_1.fechatope)
