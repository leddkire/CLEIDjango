
def guardarPersona(persona,form):
    persona.nombre = form.cleaned_data['nombre']
    persona.apellido = form.cleaned_data['apellido']
    persona.correo = form.cleaned_data['correo']
    persona.dirpostal = form.cleaned_data['dirpostal']
    persona.institucion = form.cleaned_data['institucion']
    persona.telefono = form.cleaned_data['telefono']
    persona.pais = form.cleaned_data['pais']
    persona.pagina = form.cleaned_data['pagina']
    persona.save()
    return persona