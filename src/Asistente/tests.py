from django.test import TestCase
from Persona.models import Persona
from Asistente.models import Asistente
import unittest

# Create your tests here.

class Test(TestCase):

   def testAsistente(self):
        p = Persona(correo = "patty@usb.ve", dirpostal = 1090)
        a = Asistente(persona = p)
        self.assertEqual(p, a.persona)
