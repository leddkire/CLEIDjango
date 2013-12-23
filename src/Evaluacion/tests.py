from django.test import TestCase
from Evaluacion.models import Evaluacion, Nota
from Articulo.models import Articulo
from Autor.models import Autor
from Topico.models import Topico
from Comite.models import Comite
from Persona.models import Persona

class EvaluacionTestCase(TestCase):
    
    def test_nota(self):
        n = Nota(valor = 5)
        self.assertEqual(n.valor, 5)
        
    def test_evaluacion(self):
        p = Persona(correo = "eznex7@gmail.com", dirpostal = 5020)
        a = Comite(correo = p, presidente = False, arbitro = True)
        ar = Articulo(titulo = "Base de Datos: Web Semantica")
        ar.save()
        n = Nota(valor = 5)
        n.save()
        a.save()
        e = Evaluacion(articulo = ar, promedio = 5.0)
        e.save()
        e.notas.add(n)
        e.arbitros.add(a)
        self.assertEqual(e.articulo, ar)
        self.assertEqual(e.notas.all()[0], n)
        self.assertEqual(e.arbitros.all()[0], a)
        self.assertEqual(e.promedio, 5.0)
    
    def test_evaluacionVista(self):
        p = Persona(correo = "eznex7@gmail.com", dirpostal = 5020)
        a = Comite(correo = p, presidente = False, arbitro = True)
        ar = Articulo(titulo = "Base de Datos: Web Semantica")
        ar.save()
        n = Nota(valor = 5)
        n.save()
        a.save()
        e = Evaluacion(articulo = ar, promedio = 5.0)
        e.save()
        e.notas.add(n)
        e.arbitros.add(a)
        resp = self.client.get('/evaluacion/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('evaluaciones' in resp.context)
        self.assertEqual(len(resp.context['evaluaciones']),1)
        evaluacion_1 = resp.context['evaluaciones'][0]
        self.assertEqual(evaluacion_1.articulo, ar)
        self.assertEqual(evaluacion_1.notas.all()[0], n)
        self.assertEqual(evaluacion_1.arbitros.all()[0], a)
        self.assertEqual(evaluacion_1.promedio, 5.0)

