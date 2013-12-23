from django.test import TestCase
from Persona.models import Persona
from Autor.models import Autor

class AutorTestCase(TestCase):
    def test_autor(self):
        p = Persona(correo = "eznex7@gmail.com", dirpostal = 5020)
        a = Autor(persona = p)
        self.assertEqual(a.persona, p)