from django.test import TestCase
from Persona.models import Persona
from Autor.models import Autor
from Articulo.models import Articulo
from Topico.models import Topico

class ArticuloTestCase(TestCase):
    def test_articulo(self):
        t = Topico(nombre = "Base de Datos")
        t.save()
        p = Persona(correo = "eznex7@gmail.com", dirpostal = 5020)
        a = Autor(persona = p)
        a.save()
        ar = Articulo(titulo = "Base de Datos: Web Semantica", palabrasClaves = "datos", resumen = "Resumen de paper", 
                    texto = "la importancia de la Web semantica...", aceptado = True, aceptable = True, empatado = False)
        ar.save()
        ar.topicos.add(t)
        ar.autores.add(a)
        self.assertEqual(ar.titulo, "Base de Datos: Web Semantica")
        self.assertEqual(ar.palabrasClaves, "datos")
        self.assertEqual(ar.resumen, "Resumen de paper")
        self.assertEqual(ar.texto, "la importancia de la Web semantica...")
        self.assertEqual(ar.autores.all()[0], a)
        self.assertEqual(ar.topicos.all()[0], t)
        self.assertEqual(ar.aceptado, True)
        self.assertEqual(ar.aceptable, True)
        self.assertEqual(ar.empatado, False)
        
    def test_articuloVista(self):
        t = Topico(nombre = "Base de Datos")
        t.save()
        p = Persona(correo = "eznex7@gmail.com", dirpostal = 5020)
        a = Autor(persona = p)
        a.save()
        ar = Articulo(titulo = "Base de Datos: Web Semantica", palabrasClaves = "datos", resumen = "Resumen de paper", 
                    texto = "la importancia de la Web semantica...", aceptado = True, aceptable = True, empatado = False)
        ar.save()
        ar.topicos.add(t)
        ar.autores.add(a)
        
        ar.save()
        resp = self.client.get('/articulo/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('articulos' in resp.context)
        self.assertEqual(len(resp.context['articulos']), 1)
        articulo_1 = resp.context['articulos'][0]
        self.assertEqual(articulo_1.titulo, "Base de Datos: Web Semantica")
        self.assertEqual(articulo_1.palabrasClaves, "datos")
        self.assertEqual(articulo_1.resumen, "Resumen de paper")
        self.assertEqual(articulo_1.texto, "la importancia de la Web semantica...")
        self.assertEqual(articulo_1.autores.all()[0], a)
        self.assertEqual(articulo_1.topicos.all()[0], t)
        self.assertEqual(articulo_1.aceptado, True)
        self.assertEqual(articulo_1.aceptable, True)
        self.assertEqual(articulo_1.empatado, False)