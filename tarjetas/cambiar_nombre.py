import os
import re

def eliminar_ces(variable):
    patron = r'[^a-zA-Z0-9\s]'  # Patrón para buscar caracteres especiales
    variable_sin_caracteres = re.sub(patron, '', variable)
    return variable_sin_caracteres


def cambiar_nombre_imagen(instance, filename):
    # Generar un nombre único utilizando UUID
    nombre_ces = eliminar_ces(os.path.splitext(filename)[0])
    nombre_archivo = nombre_ces  
    
    # Obtener la extensión del archivo original
    extension = os.path.splitext(filename)[1]
    
    # Concatenar el nombre único con la extensión original
    nuevo_nombre = nombre_archivo + extension
    
    # Devolver la ruta completa del archivo
    return os.path.join('imagen_file/', nuevo_nombre)