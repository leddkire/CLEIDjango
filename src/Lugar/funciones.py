from Lugar.models import Lugar

def existe(nombreL):
    return Lugar.objects.filter(nombre=nombreL).exists()