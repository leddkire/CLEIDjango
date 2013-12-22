from Evaluacion.models import Evaluacion
from Comite.models import Comite

def existe(correoA,tituloA):
    print correoA
    arbitroId=Comite.objects.get(correo=correoA).id
    evaluo=Evaluacion.objects.filter(arbitros__pk=arbitroId,articulo__titulo=tituloA).exists()
    return evaluo