from django.test import TestCase
from Persona.models import Persona

class PersonaTestCase(TestCase):
    def test_persona(self):
        p = Persona(nombre = "Ezequiel", apellido = "Gimenez", correo = "eze@gmail.com", dirpostal = 5020, 
                    institucion = "USB", telefono = "04242042547", pais = "Venezuela", pagina = "NA")
        self.assertEqual(p.nombre, "Ezequiel")
        self.assertEqual(p.apellido, "Gimenez")
        self.assertEqual(p.correo, "eze@gmail.com")
        self.assertEqual(p.dirpostal, 5020)
        self.assertEqual(p.institucion, "USB")
        self.assertEqual(p.telefono, "04242042547")
        self.assertEqual(p.pais, "Venezuela")
        self.assertEqual(p.pagina, "NA")
    
    def test_personaVista(self):
        p = Persona(nombre = "Ezequiel", apellido = "Gimenez", correo = "eze@gmail.com", dirpostal = 5020, 
                    institucion = "USB", telefono = "04242042547", pais = "Venezuela", pagina = "NA")
        p.save()
        resp = self.client.get('/persona/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('persona' in resp.context)
        self.assertEqual([persona.pk for persona in resp.context['persona']], ["eze@gmail.com"])
        persona_1 = resp.context['persona'][0]
        self.assertEqual(persona_1.nombre, "Ezequiel")
        self.assertEqual(persona_1.apellido, "Gimenez")
        self.assertEqual(persona_1.correo, "eze@gmail.com")
        self.assertEqual(persona_1.dirpostal, 5020)
        self.assertEqual(persona_1.institucion, "USB")
        self.assertEqual(persona_1.telefono, "04242042547")
        self.assertEqual(persona_1.pais, "Venezuela")
        self.assertEqual(persona_1.pagina, "NA")
        
    def test_mostrarFormPersonaVista(self):
        p = Persona(nombre = "Ezequiel", apellido = "Gimenez", correo = "eze@gmail.com", dirpostal = 5020, 
                    institucion = "USB", telefono = "04242042547", pais = "Venezuela", pagina = "NA")
        p.save()
        resp = self.client.get('/persona/mostrarFormPersona', follow = True)
        self.assertEqual(resp.status_code, 200)
    
    def test_crearVista(self):
        p = Persona(nombre = "Ezequiel", apellido = "Gimenez", correo = "eze@gmail.com", dirpostal = 5020, 
                    institucion = "USB", telefono = "04242042547", pais = "Venezuela", pagina = "NA")
        p.save()
        resp = self.client.get('/persona/crear', follow = True)
        self.assertEqual(resp.status_code, 200)