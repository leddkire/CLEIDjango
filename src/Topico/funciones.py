from Topico.models import Topico

def existe(nombreT):
    return Topico.objects.filter(nombre=nombreT).exists()