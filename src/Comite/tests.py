from django.test import TestCase
from Persona.models import Persona
from Comite.models import Comite

class ComiteTestCase(TestCase):
    def test_comite(self):
        p = Persona(correo = "eznex7@gmail.com", dirpostal = 5020)
        c = Comite(correo = p, presidente = False, arbitro = True)
        self.assertEqual(c.correo, p)
        self.assertEqual(c.presidente, False)
        self.assertEqual(c.arbitro, True)
        
    def test_comiteVista(self):
        persona_1 = Persona.objects.create(
                                           correo = "eznex7@gmail.com",
                                           dirpostal = 5020)
        comite_1 = Comite.objects.create(
                                         correo = persona_1,
                                         presidente = False,
                                         arbitro = True)
        
        resp = self.client.get('/comite/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('comite' in resp.context)
        self.assertEqual([comite.pk for comite in resp.context['comite']], [1])
        comite_1 = resp.context['comite'][0]
        self.assertEqual(comite_1.correo, persona_1)
        self.assertEqual(comite_1.presidente, False)
        self.assertEqual(comite_1.arbitro, True)