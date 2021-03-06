from django.test import TestCase
from Evento.models import Evento
from Evento.models import Apertura, Taller, Ponencia, CharlaInvitada
from Topico.models import Topico
from Lugar.models import Lugar
from datetime import date
from datetime import time
from Persona.models import Persona
from Comite.models import Comite, Moderador

class EventoTestCase(TestCase):
    def test_evento(self):
        d = '2013-12-22'
        t = '1:0:0'
        l = Lugar(nombre = "Caracas", ubicacion = "Mys 213", capacidadMax = 30)
        e = Evento(lugar = l, titulo = "Exposicion", duracion = 2, fechaIni = d, horaIni = t)
        self.assertEqual(e.lugar, l)
        self.assertEqual(e.titulo, "Exposicion")
        self.assertEqual(e.duracion, 2)
        self.assertEqual(e.fechaIni, d)
        self.assertEqual(e.horaIni, t)
    
    def test_EventoVistas(self):
        d = '2013-12-22'
        t = '1:0:0'
        l = Lugar(nombre = "Caracas", ubicacion = "Mys 213", capacidadMax = 30)
        l.save()
        e = Apertura(lugar = l, titulo = "Exposicion", duracion = 2, fechaIni = d, horaIni = t)
        e.save()
        resp = self.client.get('/evento/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('apertura' in resp.context)
        self.assertEqual([evento.pk for evento in resp.context['apertura']], [1])
        apertura_1 = resp.context['apertura'][0]
        self.assertEqual(apertura_1.lugar, l)
        self.assertEqual(apertura_1.titulo, "Exposicion")
        self.assertEqual(apertura_1.duracion, 2)
        self.assertEqual(apertura_1.fechaIni, date(2013,12,22))
        self.assertEqual(apertura_1.horaIni, time(1,0,0))
        
        resp = self.client.get('/evento/1/apertura', follow = True)
        self.assertEqual(resp.status_code, 200)
        
    def test_Taller(self):
        topico_1 = Topico(nombre = "Ingenieria de Software")
        topico_1.save()
        d = '2013-12-22'
        t = '1:0:0'
        l = Lugar(nombre = "Caracas", ubicacion = "Mys 213", capacidadMax = 30)
        l.save()
        e = Taller(lugar = l, titulo = "Exposicion", duracion = 2, fechaIni = d, horaIni = t,
                   topico = topico_1)
        e.save()
        resp = self.client.get('/evento/')
        self.assertEqual(resp.status_code, 200)
    
    def test_Ponencia(self):
        topico_1 = Topico(nombre = "Ingenieria de Software")
        topico_1.save()
        p = Persona(correo = "eznex7@gmail.com", dirpostal = 5020)
        p.save()
        c = Comite(correo = p, presidente = False, arbitro = True)
        c.save()
        m = Moderador(comite = c)
        m.save()
        d = '2013-12-22'
        t = '1:0:0'
        l = Lugar(nombre = "Caracas", ubicacion = "Mys 213", capacidadMax = 30)
        l.save()
        e = Ponencia(lugar = l, titulo = "Exposicion", duracion = 2, fechaIni = d, horaIni = t,
                   topico = topico_1)
        e.save()
        e.moderadores.add(m)
        resp = self.client.get('/evento/')
        self.assertEqual(resp.status_code, 200)
        
    def test_CharlaInvitada(self):
        topico_1 = Topico(nombre = "Ingenieria de Software")
        topico_1.save()
        p = Persona(correo = "eznex7@gmail.com", dirpostal = 5020)
        p.save()
        c = Comite(correo = p, presidente = False, arbitro = True)
        c.save()
        m = Moderador(comite = c)
        m.save()
        d = '2013-12-22'
        t = '1:0:0'
        l = Lugar(nombre = "Caracas", ubicacion = "Mys 213", capacidadMax = 30)
        l.save()
        e = CharlaInvitada(lugar = l, titulo = "Exposicion", duracion = 2, fechaIni = d, horaIni = t,
                   topico = topico_1)
        e.save()
        e.moderadores.add(m)
        resp = self.client.get('/evento/')
        self.assertEqual(resp.status_code, 200)