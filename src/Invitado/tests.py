from django.test import TestCase
from Invitado.models import Invitado
from Persona.models import Persona

class InvitadoTestCase(TestCase):
    def test_invitado(self):
        p = Persona(correo = "eznex7@gmail.com", dirpostal = 5020)
        i = Invitado(correo = p, cv = "Estudia en la USB")
        self.assertEqual(i.correo, p)
        self.assertEqual(i.cv, "Estudia en la USB")
    
    def test_InvitadoVista(self):
        p = Persona(correo = "eznex7@gmail.com", dirpostal = 5020)
        i = Invitado(correo = p, cv = "Estudia en la USB")
        p.save()
        i.save()
        resp = self.client.get('/invitado/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('invitado' in resp.context)
        self.assertEqual([invitado.pk for invitado in resp.context['invitado']], [1])
        invitado_1 = resp.context['invitado'][0]
        self.assertEqual(invitado_1.correo, p)
        self.assertEqual(invitado_1.cv, "Estudia en la USB")
