"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_asignarModeradorVista(self):
        resp = self.client.get('/asignarModerador/')
        self.assertEqual(resp.status_code, 200)
        
