"""
Modelos para el Sistema de CV Profesional
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.text import slugify

import uuid


# ======================================
# MODELO: PERFIL PROFESIONAL
# ======================================

class PerfilProfesional(models.Model):
    """
    Información personal y profesional del usuario
    """
    NIVEL_EXPERIENCIA_CHOICES = [
        ('junior', 'Junior (0-2 años)'),
        ('mid', 'Mid-Level (3-5 años)'),
        ('senior', 'Senior (6-10 años)'),
        ('lead', 'Lead/Principal (10+ años)'),
    ]
    
    # Relación con usuario
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Información personal
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de Nacimiento')
    nacionalidad = models.CharField(max_length=50, default='Ecuatoriana', verbose_name='Nacionalidad')
    
    # Foto de perfil con procesamiento automático
    foto = models.ImageField(
    upload_to='profile_photos/',
    null=True,
    blank=True,
    verbose_name='Foto de Perfil'
)

    
    # Contacto
    email = models.EmailField(verbose_name='Email Profesional')
    telefono = PhoneNumberField(region='EC', verbose_name='Teléfono')
    linkedin = models.URLField(max_length=200, blank=True, verbose_name='LinkedIn')
    github = models.URLField(max_length=200, blank=True, verbose_name='GitHub')
    portafolio_web = models.URLField(max_length=200, blank=True, verbose_name='Portafolio Web')
    
    # Ubicación
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
    provincia = models.CharField(max_length=100, verbose_name='Provincia/Estado')
    pais = models.CharField(max_length=100, default='Ecuador', verbose_name='País')
    
    # Profesión
    titulo_profesional = models.CharField(max_length=150, verbose_name='Título Profesional')
    nivel_experiencia = models.CharField(max_length=10, choices=NIVEL_EXPERIENCIA_CHOICES, default='mid')
    anos_experiencia = models.PositiveIntegerField(default=0, verbose_name='Años de Experiencia')
    
    # Resumen profesional
    resumen_profesional = models.TextField(max_length=500, verbose_name='Resumen Profesional')
    objetivo_profesional = models.TextField(max_length=300, blank=True, verbose_name='Objetivo Profesional')
    
    # Configuración de privacidad
    cv_publico = models.BooleanField(default=False, verbose_name='CV Público')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    from datetime import date
    from django.core.exceptions import ValidationError

    def clean(self):
        if not self.fecha_nacimiento:
            return

        hoy = date.today()

        if self.fecha_nacimiento > hoy:
            raise ValidationError(
                {"fecha_nacimiento": "La fecha de nacimiento no puede ser futura."}
            )

        edad = hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

        if edad < 15:
            raise ValidationError(
                {"fecha_nacimiento": "La edad mínima permitida es de 15 años."}
            )

        if edad > 75:
            raise ValidationError(
                {"fecha_nacimiento": "La edad ingresada no es válida."}
            )


    
    class Meta:
        verbose_name = 'Perfil Profesional'
        verbose_name_plural = 'Perfiles Profesionales'
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.nombres} {self.apellidos}")
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"

        super().save(*args, **kwargs)


        

    
    def get_absolute_url(self):
        return reverse('curriculum:ver_cv', kwargs={'slug': self.slug})
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"


# ======================================
# MODELO: FORMACIÓN ACADÉMICA
# ======================================

class FormacionAcademica(models.Model):
    """
    Educación formal del usuario
    """
    NIVEL_EDUCACION_CHOICES = [
        ('bachillerato', 'Bachillerato'),
        ('tecnico', 'Técnico/Tecnólogo'),
        ('pregrado', 'Pregrado/Licenciatura'),
        ('especializacion', 'Especialización'),
        ('maestria', 'Maestría'),
        ('doctorado', 'Doctorado'),
    ]
    
    ESTADO_CHOICES = [
        ('cursando', 'Cursando'),
        ('completado', 'Completado'),
        ('incompleto', 'Incompleto'),
    ]
    
    perfil = models.ForeignKey(PerfilProfesional, on_delete=models.CASCADE, related_name='formacion_academica')
    
    nivel = models.CharField(max_length=20, choices=NIVEL_EDUCACION_CHOICES, verbose_name='Nivel de Educación')
    titulo_obtenido = models.CharField(max_length=200, verbose_name='Título Obtenido')
    institucion = models.CharField(max_length=200, verbose_name='Institución Educativa')
    
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_fin = models.DateField(null=True, blank=True, verbose_name='Fecha de Finalización')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='completado')
    
    promedio = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Promedio/GPA'
    )
    
    descripcion = models.TextField(max_length=500, blank=True, verbose_name='Descripción')
    certificado = models.FileField(
        upload_to='certificates/education/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        verbose_name='Certificado (PDF)'
    )
    
    orden = models.PositiveIntegerField(default=0, verbose_name='Orden de visualización')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Formación Académica'
        verbose_name_plural = 'Formación Académica'
        ordering = ['-fecha_inicio', 'orden']
    
    def __str__(self):
        return f"{self.titulo_obtenido} - {self.institucion}"
    
    def clean(self):
        hoy = date.today()

        if self.fecha_inicio > hoy:
            raise ValidationError("La fecha de inicio no puede ser futura.")

        if self.fecha_fin:
            if self.fecha_fin > hoy:
                raise ValidationError("La fecha de finalización no puede ser futura.")
            if self.fecha_fin < self.fecha_inicio:
                raise ValidationError("La fecha de finalización no puede ser anterior a la de inicio.")




# ======================================
# MODELO: EXPERIENCIA PROFESIONAL
# ======================================

class ExperienciaProfesional(models.Model):
    """
    Experiencia laboral del usuario
    """
    TIPO_EMPLEO_CHOICES = [
        ('tiempo_completo', 'Tiempo Completo'),
        ('medio_tiempo', 'Medio Tiempo'),
        ('freelance', 'Freelance'),
        ('contrato', 'Contrato'),
        ('pasantia', 'Pasantía'),
    ]
    
    perfil = models.ForeignKey(PerfilProfesional, on_delete=models.CASCADE, related_name='experiencias')
    
    cargo = models.CharField(max_length=150, verbose_name='Cargo/Posición')
    empresa = models.CharField(max_length=200, verbose_name='Empresa')
    tipo_empleo = models.CharField(max_length=20, choices=TIPO_EMPLEO_CHOICES, default='tiempo_completo')
    
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
    pais = models.CharField(max_length=100, default='Ecuador', verbose_name='País')
    
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_fin = models.DateField(null=True, blank=True, verbose_name='Fecha de Finalización')
    trabajo_actual = models.BooleanField(default=False, verbose_name='Trabajo Actual')
    
    descripcion = models.TextField(max_length=1000, verbose_name='Descripción de Responsabilidades')
    logros = models.TextField(max_length=1000, blank=True, verbose_name='Logros Principales')
    
    tecnologias_usadas = models.CharField(max_length=500, blank=True, verbose_name='Tecnologías Utilizadas')
    
    orden = models.PositiveIntegerField(default=0)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Experiencia Profesional'
        verbose_name_plural = 'Experiencias Profesionales'
        ordering = ['-fecha_inicio', 'orden']
    
    def __str__(self):
        return f"{self.cargo} en {self.empresa}"
    
    def save(self, *args, **kwargs):
        if self.trabajo_actual:
            self.fecha_fin = None
        super().save(*args, **kwargs)
    
    def clean(self):
        hoy = date.today()

        if self.fecha_inicio > hoy:
            raise ValidationError("La fecha de inicio no puede ser futura.")

        if self.fecha_fin:
            if self.fecha_fin > hoy:
                raise ValidationError("La fecha de finalización no puede ser futura.")
            if self.fecha_fin < self.fecha_inicio:
                raise ValidationError("La fecha de finalización no puede ser anterior a la de inicio.")




# ======================================
# MODELO: HABILIDADES
# ======================================

class Habilidad(models.Model):
    """
    Habilidades técnicas y blandas
    """
    TIPO_HABILIDAD_CHOICES = [
        ('tecnica', 'Habilidad Técnica'),
        ('blanda', 'Habilidad Blanda'),
        ('idioma', 'Idioma'),
        ('herramienta', 'Herramienta/Software'),
    ]
    
    perfil = models.ForeignKey(PerfilProfesional, on_delete=models.CASCADE, related_name='habilidades')
    
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Habilidad')
    tipo = models.CharField(max_length=15, choices=TIPO_HABILIDAD_CHOICES, default='tecnica')
    nivel = models.PositiveIntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Nivel de Dominio (%)',
        help_text='0 = Básico, 50 = Intermedio, 100 = Experto'
    )
    
    anos_experiencia = models.PositiveIntegerField(default=0,validators=[MaxValueValidator(55)], verbose_name='Años de Experiencia')
    descripcion = models.TextField(max_length=200, blank=True, verbose_name='Descripción')
    
    # Para certificaciones
    certificado = models.FileField(
        upload_to='certificates/skills/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name='Certificado'
    )
    
    orden = models.PositiveIntegerField(default=0)
    destacada = models.BooleanField(default=False, verbose_name='Habilidad Destacada')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'
        ordering = ['-destacada', 'tipo', '-nivel', 'orden']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()}) - {self.nivel}%"


# ======================================
# MODELO: PROYECTOS
# ======================================

class Proyecto(models.Model):
    """
    Proyectos destacados del usuario
    """
    ESTADO_CHOICES = [
        ('en_desarrollo', 'En Desarrollo'),
        ('completado', 'Completado'),
        ('mantenimiento', 'En Mantenimiento'),
        ('archivado', 'Archivado'),
    ]
    
    perfil = models.ForeignKey(PerfilProfesional, on_delete=models.CASCADE, related_name='proyectos')
    
    nombre = models.CharField(max_length=200, verbose_name='Nombre del Proyecto')
    descripcion_corta = models.CharField(max_length=200, verbose_name='Descripción Corta')
    descripcion = models.TextField(max_length=1000, verbose_name='Descripción Detallada')
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='completado')
    
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_fin = models.DateField(null=True, blank=True, verbose_name='Fecha de Finalización')
    
    rol = models.CharField(max_length=100, verbose_name='Tu Rol', help_text='Ej: Desarrollador Full Stack')
    tecnologias = models.CharField(max_length=500, verbose_name='Tecnologías Utilizadas')
    
    # Enlaces
    url_demo = models.URLField(max_length=200, blank=True, verbose_name='URL Demo/Sitio')
    url_repositorio = models.URLField(max_length=200, blank=True, verbose_name='Repositorio (GitHub/GitLab)')
    
    # Imagen del proyecto
    imagen = models.ImageField(
    upload_to='project_images/',
    null=True,
    blank=True,
    verbose_name='Imagen del Proyecto'
)

    
    destacado = models.BooleanField(default=False, verbose_name='Proyecto Destacado')
    orden = models.PositiveIntegerField(default=0)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-destacado', '-fecha_inicio', 'orden']
    
    def __str__(self):
        return self.nombre
    
    def clean(self):
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")



# ======================================
# MODELO: REFERENCIAS PROFESIONALES
# ======================================

class ReferenciaProfesional(models.Model):
    """
    Referencias de colegas o superiores
    """
    perfil = models.ForeignKey(PerfilProfesional, on_delete=models.CASCADE, related_name='referencias')
    
    nombre_completo = models.CharField(max_length=150, verbose_name='Nombre Completo')
    cargo = models.CharField(max_length=150, verbose_name='Cargo')
    empresa = models.CharField(max_length=200, verbose_name='Empresa')
    
    relacion = models.CharField(
        max_length=200, 
        verbose_name='Relación Profesional',
        help_text='Ej: Ex-supervisor directo, Colega de equipo'
    )
    
    email = models.EmailField(verbose_name='Email')
    telefono = PhoneNumberField(region='EC', verbose_name='Teléfono')
    linkedin = models.URLField(max_length=200, blank=True, verbose_name='LinkedIn')
    
    testimonio = models.TextField(max_length=500, blank=True, verbose_name='Testimonio/Recomendación')
    
    # Configuración de privacidad
    mostrar_contacto = models.BooleanField(
        default=False, 
        verbose_name='Mostrar Información de Contacto',
        help_text='Si está desactivado, solo se mostrará el nombre y cargo'
    )
    
    orden = models.PositiveIntegerField(default=0)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Referencia Profesional'
        verbose_name_plural = 'Referencias Profesionales'
        ordering = ['orden', '-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre_completo} - {self.cargo} en {self.empresa}"


# ======================================
# MODELO: CERTIFICACIONES
# ======================================

class Certificacion(models.Model):
    """
    Certificaciones y cursos adicionales
    """
    perfil = models.ForeignKey(PerfilProfesional, on_delete=models.CASCADE, related_name='certificaciones')
    
    nombre = models.CharField(max_length=200, verbose_name='Nombre de la Certificación/Curso')
    institucion = models.CharField(max_length=200, verbose_name='Institución/Plataforma')
    
    fecha_obtencion = models.DateField(verbose_name='Fecha de Obtención')
    fecha_expiracion = models.DateField(null=True, blank=True, verbose_name='Fecha de Expiración')
    
    codigo_credencial = models.CharField(max_length=100, blank=True, verbose_name='Código de Credencial')
    url_verificacion = models.URLField(max_length=200, blank=True, verbose_name='URL de Verificación')
    
    descripcion = models.TextField(max_length=500, blank=True, verbose_name='Descripción')
    
    certificado = models.FileField(
        upload_to='certificates/certifications/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name='Certificado'
    )
    
    orden = models.PositiveIntegerField(default=0)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Certificación'
        verbose_name_plural = 'Certificaciones'
        ordering = ['-fecha_obtencion', 'orden']
    
    def __str__(self):
        return f"{self.nombre} - {self.institucion}"
    
    @property
    def esta_vigente(self):
        if not self.fecha_expiracion:
            return True
        from datetime.date import today
        return self.fecha_expiracion > today()
    
    def clean(self):
        if self.fecha_expiracion and self.fecha_expiracion < self.fecha_obtencion:
            raise ValidationError("La fecha de expiración no puede ser anterior a la fecha de obtención.")
