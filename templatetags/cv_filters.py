"""
Template tags y filtros personalizados para CV
"""

from django import template
from django.utils.safestring import mark_safe
from datetime import date, datetime
import re

register = template.Library()


@register.filter(name='calcular_edad')
def calcular_edad(fecha_nacimiento):
    """
    Calcula la edad a partir de una fecha de nacimiento
    Uso: {{ perfil.fecha_nacimiento|calcular_edad }}
    """
    if not fecha_nacimiento:
        return None
    
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    
    if hoy.month < fecha_nacimiento.month or (hoy.month == fecha_nacimiento.month and hoy.day < fecha_nacimiento.day):
        edad -= 1
    
    return edad


@register.filter(name='calcular_duracion')
def calcular_duracion(fecha_inicio, fecha_fin=None):
    """
    Calcula la duración entre dos fechas en años y meses
    Uso: {{ experiencia.fecha_inicio|calcular_duracion:experiencia.fecha_fin }}
    """
    if not fecha_inicio:
        return ""
    
    if not fecha_fin:
        fecha_fin = date.today()
    
    anos = fecha_fin.year - fecha_inicio.year
    meses = fecha_fin.month - fecha_inicio.month
    
    if meses < 0:
        anos -= 1
        meses += 12
    
    if anos > 0 and meses > 0:
        return f"{anos} año{'s' if anos > 1 else ''} y {meses} mes{'es' if meses > 1 else ''}"
    elif anos > 0:
        return f"{anos} año{'s' if anos > 1 else ''}"
    elif meses > 0:
        return f"{meses} mes{'es' if meses > 1 else ''}"
    else:
        return "Menos de un mes"


@register.filter(name='nivel_color')
def nivel_color(nivel):
    """
    Retorna un color según el nivel de habilidad
    Uso: {{ habilidad.nivel|nivel_color }}
    """
    if nivel >= 80:
        return 'success'
    elif nivel >= 60:
        return 'info'
    elif nivel >= 40:
        return 'warning'
    else:
        return 'danger'


@register.filter(name='nivel_color_hex')
def nivel_color_hex(nivel):
    """
    Retorna un color hexadecimal según el nivel
    """
    if nivel >= 80:
        return '#28a745'
    elif nivel >= 60:
        return '#17a2b8'
    elif nivel >= 40:
        return '#ffc107'
    else:
        return '#dc3545'


@register.filter(name='nivel_texto')
def nivel_texto(nivel):
    """
    Convierte un nivel numérico a texto
    """
    if nivel >= 90:
        return 'Experto'
    elif nivel >= 70:
        return 'Avanzado'
    elif nivel >= 50:
        return 'Intermedio'
    elif nivel >= 30:
        return 'Básico'
    else:
        return 'Principiante'


@register.filter(name='truncar_palabras_custom')
def truncar_palabras_custom(texto, num_palabras):
    """
    Trunca texto a un número específico de palabras
    Uso: {{ descripcion|truncar_palabras_custom:20 }}
    """
    if not texto:
        return ""
    
    palabras = texto.split()
    if len(palabras) <= num_palabras:
        return texto
    
    return ' '.join(palabras[:num_palabras]) + '...'


@register.filter(name='formatear_telefono')
def formatear_telefono(telefono):
    """
    Formatea un número de teléfono
    """
    if not telefono:
        return ""
    
    # Eliminar caracteres no numéricos
    digitos = re.sub(r'\D', '', str(telefono))
    
    # Formatear según longitud
    if len(digitos) == 10:
        return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
    elif len(digitos) == 9:
        return f"{digitos[:2]} {digitos[2:5]} {digitos[5:]}"
    else:
        return telefono


@register.filter(name='icono_red_social')
def icono_red_social(url):
    """
    Retorna el icono de Bootstrap Icons según la URL
    """
    if not url:
        return 'bi-link-45deg'
    
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


@register.filter(name='primera_letra')
def primera_letra(texto):
    """
    Retorna la primera letra de un texto
    """
    return texto[0].upper() if texto else ''


@register.filter(name='iniciales')
def iniciales(nombre_completo):
    """
    Obtiene las iniciales de un nombre
    Uso: {{ perfil.nombre_completo|iniciales }}
    """
    if not nombre_completo:
        return 'CV'
    
    palabras = nombre_completo.split()
    if len(palabras) >= 2:
        return f"{palabras[0][0]}{palabras[-1][0]}".upper()
    elif len(palabras) == 1:
        return palabras[0][:2].upper()
    return 'CV'


@register.filter(name='url_dominio')
def url_dominio(url):
    """
    Extrae el dominio de una URL
    """
    if not url:
        return ""
    
    # Remover protocolo
    dominio = re.sub(r'https?://', '', url)
    # Remover www
    dominio = re.sub(r'^www\.', '', dominio)
    # Remover path
    dominio = dominio.split('/')[0]
    
    return dominio


@register.filter(name='porcentaje_completitud')
def porcentaje_completitud(perfil):
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


@register.filter(name='mes_nombre')
def mes_nombre(fecha):
    """
    Retorna el nombre del mes en español
    """
    if not fecha:
        return ""
    
    meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    
    return meses[fecha.month - 1]


@register.filter(name='ano_mes')
def ano_mes(fecha):
    """
    Formato: Enero 2024
    """
    if not fecha:
        return ""
    
    return f"{mes_nombre(fecha)} {fecha.year}"


@register.simple_tag
def progreso_cv(perfil):
    """
    Tag para obtener el progreso del CV con detalles
    Uso: {% progreso_cv perfil as progreso %}
    """
    return porcentaje_completitud(perfil)


@register.simple_tag
def skill_color_badge(nivel):
    """
    Retorna una clase de badge según el nivel
    """
    if nivel >= 80:
        return 'bg-success'
    elif nivel >= 60:
        return 'bg-info'
    elif nivel >= 40:
        return 'bg-warning'
    else:
        return 'bg-danger'


@register.inclusion_tag('curriculum/components/skill_bar.html')
def render_skill_bar(habilidad):
    """
    Renderiza una barra de habilidad
    Uso: {% render_skill_bar habilidad %}
    """
    return {
        'habilidad': habilidad,
        'color': nivel_color_hex(habilidad.nivel),
        'texto': nivel_texto
