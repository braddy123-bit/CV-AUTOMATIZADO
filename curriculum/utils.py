"""
Funciones auxiliares para el sistema de CV
"""

from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import os


def validar_tamano_imagen(archivo):
    """
    Valida que una imagen no supere el tamaño máximo permitido
    """
    limite_mb = 5
    if archivo.size > limite_mb * 1024 * 1024:
        raise ValidationError(f'La imagen no puede superar {limite_mb}MB')


def validar_tamano_pdf(archivo):
    """
    Valida que un PDF no supere el tamaño máximo permitido
    """
    limite_mb = 10
    if archivo.size > limite_mb * 1024 * 1024:
        raise ValidationError(f'El archivo PDF no puede superar {limite_mb}MB')


def get_upload_path_foto(instance, filename):
    """
    Genera ruta personalizada para fotos de perfil
    """
    extension = filename.split('.')[-1]
    nuevo_nombre = f"perfil_{instance.usuario.id}.{extension}"
    return os.path.join('profile_photos', nuevo_nombre)


def get_upload_path_certificado(instance, filename):
    """
    Genera ruta personalizada para certificados
    """
    usuario_id = instance.perfil.usuario.id
    extension = filename.split('.')[-1]
    nombre_tipo = instance.__class__.__name__.lower()
    nuevo_nombre = f"{nombre_tipo}_{instance.id}_{filename}"
    return os.path.join('certificates', str(usuario_id), nuevo_nombre)


def get_upload_path_proyecto(instance, filename):
    """
    Genera ruta personalizada para imágenes de proyectos
    """
    usuario_id = instance.perfil.usuario.id
    extension = filename.split('.')[-1]
    nuevo_nombre = f"proyecto_{instance.id}.{extension}"
    return os.path.join('project_images', str(usuario_id), nuevo_nombre)


def calcular_anos_experiencia(fecha_inicio, fecha_fin=None):
    """
    Calcula años de experiencia entre dos fechas
    """
    from datetime import date
    
    if fecha_fin is None:
        fecha_fin = date.today()
    
    anos = fecha_fin.year - fecha_inicio.year
    
    # Ajustar si aún no se ha cumplido el aniversario este año
    if fecha_fin.month < fecha_inicio.month or \
       (fecha_fin.month == fecha_inicio.month and fecha_fin.day < fecha_inicio.day):
        anos -= 1
    
    return max(0, anos)


def obtener_edad(fecha_nacimiento):
    """
    Calcula la edad a partir de la fecha de nacimiento
    """
    from datetime import date
    
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    
    if hoy.month < fecha_nacimiento.month or \
       (hoy.month == fecha_nacimiento.month and hoy.day < fecha_nacimiento.day):
        edad -= 1
    
    return edad


def sanitizar_slug(texto):
    """
    Limpia un texto para usarlo como slug
    """
    import re
    from django.utils.text import slugify
    
    # Eliminar caracteres especiales
    texto = re.sub(r'[^\w\s-]', '', texto.lower())
    
    # Convertir a slug
    return slugify(texto)


def formatear_telefono(numero):
    """
    Formatea un número de teléfono
    """
    # Eliminar caracteres no numéricos
    digitos = ''.join(filter(str.isdigit, str(numero)))
    
    # Formatear según longitud
    if len(digitos) == 10:
        return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
    elif len(digitos) == 9:
        return f"{digitos[:2]} {digitos[2:5]} {digitos[5:]}"
    else:
        return numero


def generar_color_skill(nivel):
    """
    Genera un color según el nivel de habilidad
    """
    if nivel >= 80:
        return '#28a745'  # Verde
    elif nivel >= 60:
        return '#17a2b8'  # Azul
    elif nivel >= 40:
        return '#ffc107'  # Amarillo
    else:
        return '#dc3545'  # Rojo


def obtener_icono_red_social(url):
    """
    Devuelve el icono apropiado según la URL de red social
    """
    url = url.lower()
    
    if 'linkedin' in url:
        return 'bi-linkedin'
    elif 'github' in url:
        return 'bi-github'
    elif 'twitter' in url or 'x.com' in url:
        return 'bi-twitter-x'
    elif 'facebook' in url:
        return 'bi-facebook'
    elif 'instagram' in url:
        return 'bi-instagram'
    else:
        return 'bi-link-45deg'


def truncar_texto(texto, longitud=100):
    """
    Trunca un texto a una longitud específica
    """
    if len(texto) <= longitud:
        return texto
    return texto[:longitud].rsplit(' ', 1)[0] + '...'


def obtener_iniciales(nombre_completo):
    """
    Obtiene las iniciales de un nombre
    """
    palabras = nombre_completo.split()
    if len(palabras) >= 2:
        return f"{palabras[0][0]}{palabras[-1][0]}".upper()
    elif len(palabras) == 1:
        return palabras[0][:2].upper()
    return "CV"


def validar_url_linkedin(url):
    """
    Valida que una URL sea de LinkedIn
    """
    import re
    patron = r'(https?://)?(www\.)?linkedin\.com/in/[\w-]+'
    return bool(re.match(patron, url))


def validar_url_github(url):
    """
    Valida que una URL sea de GitHub
    """
    import re
    patron = r'(https?://)?(www\.)?github\.com/[\w-]+'
    return bool(re.match(patron, url))


def generar_descripcion_meta(perfil):
    """
    Genera una meta descripción para SEO
    """
    return f"{perfil.titulo_profesional} con {perfil.anos_experiencia} años de experiencia. {perfil.resumen_profesional[:150]}"


def obtener_porcentaje_completitud(perfil):
    """
    Calcula el porcentaje de completitud del CV
    """
    total = 10
    completado = 0
    
    # Datos personales (2 puntos)
    if perfil.foto:
        completado += 1
    if perfil.resumen_profesional:
        completado += 1
    
    # Formación (2 puntos)
    if perfil.formacion_academica.exists():
        completado += 2
    
    # Experiencia (2 puntos)
    if perfil.experiencias.exists():
        completado += 2
    
    # Habilidades (2 puntos)
    if perfil.habilidades.count() >= 5:
        completado += 2
    elif perfil.habilidades.exists():
        completado += 1
    
    # Proyectos (1 punto)
    if perfil.proyectos.exists():
        completado += 1
    
    # Certificaciones (1 punto)
    if perfil.certificaciones.exists():
        completado += 1
    
    return int((completado / total) * 100)
