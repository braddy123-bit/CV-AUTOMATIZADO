"""
Modelos para el Sistema de CV Profesional
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
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

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')

    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de Nacimiento')
    nacionalidad = models.CharField(max_length=50, default='Ecuatoriana', verbose_name='Nacionalidad')

    foto = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        verbose_name='Foto de Perfil'
    )

    email = models.EmailField(verbose_name='Email Profesional')
    telefono = PhoneNumberField(region='EC', verbose_name='Teléfono')
    linkedin = models.URLField(max_length=200, blank=True, verbose_name='LinkedIn')
    github = models.URLField(max_length=200, blank=True, verbose_name='GitHub')
    portafolio_web = models.URLField(max_length=200, blank=True, verbose_name='Portafolio Web')

    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
    provincia = models.CharField(max_length=100, verbose_name='Provincia/Estado')
    pais = models.CharField(max_length=100, default='Ecuador', verbose_name='País')

    titulo_profesional = models.CharField(max_length=150, verbose_name='Título Profesional')
    nivel_experiencia = models.CharField(max_length=10, choices=NIVEL_EXPERIENCIA_CHOICES, default='mid')
    anos_experiencia = models.PositiveIntegerField(default=0, verbose_name='Años de Experiencia')

    resumen_profesional = models.TextField(max_length=500, verbose_name='Resumen Profesional')
    objetivo_profesional = models.TextField(max_length=300, blank=True, verbose_name='Objetivo Profesional')

    cv_publico = models.BooleanField(default=False, verbose_name='CV Público')
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil Profesional'
        verbose_name_plural = 'Perfiles Profesionales'
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    def clean(self):
        if self.fecha_nacimiento:
            hoy = date.today()

            if self.fecha_nacimiento > hoy:
                raise ValidationError("La fecha de nacimiento no puede ser futura.")

            edad = hoy.year - self.fecha_nacimiento.year - (
                (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )

            if edad < 15:
                raise ValidationError("La edad mínima permitida en Ecuador es 15 años.")

            if edad > 100:
                raise ValidationError("La edad ingresada no es válida.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{self.nombres.lower()}-{self.apellidos.lower()}-{uuid.uuid4().hex[:8]}"
        self.full_clean()
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

    nivel = models.CharField(max_length=20, choices=NIVEL_EDUCACION_CHOICES)
    titulo_obtenido = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='completado')

    promedio = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    descripcion = models.TextField(max_length=500, blank=True)

    certificado = models.FileField(
        upload_to='certificates/education/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    orden = models.PositiveIntegerField(default=0)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha de finalización no puede ser anterior a la de inicio.")


# ======================================
# MODELO: EXPERIENCIA PROFESIONAL
# ======================================

class ExperienciaProfesional(models.Model):

    TIPO_EMPLEO_CHOICES = [
        ('tiempo_completo', 'Tiempo Completo'),
        ('medio_tiempo', 'Medio Tiempo'),
        ('freelance', 'Freelance'),
        ('contrato', 'Contrato'),
        ('pasantia', 'Pasantía'),
    ]

    perfil = models.ForeignKey(PerfilProfesional, on_delete=models.CASCADE, related_name='experiencias')

    cargo = models.CharField(max_length=150)
    empresa = models.CharField(max_length=200)
    tipo_empleo = models.CharField(max_length=20, choices=TIPO_EMPLEO_CHOICES, default='tiempo_completo')

    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default='Ecuador')

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    trabajo_actual = models.BooleanField(default=False)

    descripcion = models.TextField(max_length=1000)
    logros = models.TextField(max_length=1000, blank=True)
    tecnologias_usadas = models.CharField(max_length=500, blank=True)

    orden = models.PositiveIntegerField(default=0)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")

    def save(self, *args, **kwargs):
        if self.trabajo_actual:
            self.fecha_fin = None
        self.full_clean()
        super().save(*args, **kwargs)
