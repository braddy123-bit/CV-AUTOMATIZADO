"""
Modelos EXACTOS según las tablas SQL del profesor
Adaptado 100% a la estructura proporcionada
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from datetime import date
import uuid


# ======================================
# VALIDADORES
# ======================================

def validar_fecha_pasada(value):
    """No permite fechas futuras"""
    if value > date.today():
        raise ValidationError('La fecha no puede ser futura')


def validar_fecha_nacimiento(value):
    """Valida fecha de nacimiento"""
    if value > date.today():
        raise ValidationError('La fecha de nacimiento no puede ser futura')
    edad = date.today().year - value.year
    if edad < 15 or edad > 100:
        raise ValidationError('La edad debe estar entre 15 y 100 años')


# ======================================
# TABLA: DATOSPERSONALES
# ======================================

class DatosPersonales(models.Model):
    """
    Mapea: DATOSPERSONALES
    Campos EXACTOS de la tabla SQL
    """
    SEXO_CHOICES = [('H', 'Hombre'), ('M', 'Mujer')]
    
    ESTADO_CIVIL_CHOICES = [
        ('Soltero/a', 'Soltero/a'),
        ('Casado/a', 'Casado/a'),
        ('Divorciado/a', 'Divorciado/a'),
        ('Viudo/a', 'Viudo/a'),
        ('Unión Libre', 'Unión Libre'),
    ]
    
    # Usuario Django (no está en tabla SQL pero necesario)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='datos_personales')
    
    # Campos EXACTOS de la tabla SQL
    idperfil = models.AutoField(primary_key=True, db_column='idperfil')
    descripcionperfil = models.CharField(max_length=50, db_column='descripcionperfil')
    perfilactivo = models.IntegerField(default=1, db_column='perfilactivo')
    apellidos = models.CharField(max_length=60, db_column='apellidos')
    nombres = models.CharField(max_length=60, db_column='nombres')
    nacionalidad = models.CharField(max_length=20, db_column='nacionalidad')
    lugarnacimiento = models.CharField(max_length=60, db_column='lugarnacimiento')
    fechanacimiento = models.DateField(db_column='fechanacimiento', validators=[validar_fecha_nacimiento])
    numerocedula = models.CharField(max_length=10, unique=True, db_column='numerocedula')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, db_column='sexo')
    estadocivil = models.CharField(max_length=50, choices=ESTADO_CIVIL_CHOICES, db_column='estadocivil')
    licenciaconducir = models.CharField(max_length=6, db_column='licenciaconducir')
    telefonoconvencional = models.CharField(max_length=15, blank=True, db_column='telefonoconvencional')
    telefonofijo = models.CharField(max_length=15, blank=True, db_column='telefonofijo')
    direcciontrabajo = models.CharField(max_length=50, blank=True, db_column='direcciontrabajo')
    direcciondomiciliaria = models.CharField(max_length=50, db_column='direcciondomiciliaria')
    sitioweb = models.CharField(max_length=60, blank=True, db_column='sitioweb')
    
    # Campos adicionales (no en SQL pero necesarios)
    foto = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'datospersonales'
        verbose_name = 'Datos Personales'
        verbose_name_plural = 'Datos Personales'
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{self.nombres}-{self.apellidos}-{uuid.uuid4().hex[:8]}".lower()
        super().save(*args, **kwargs)
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def edad(self):
        hoy = date.today()
        return hoy.year - self.fechanacimiento.year - ((hoy.month, hoy.day) < (self.fechanacimiento.month, self.fechanacimiento.day))


# ======================================
# TABLA: EXPERIENCIALABORAL
# ======================================

class ExperienciaLaboral(models.Model):
    """
    Mapea: EXPERIENCIALABORAL
    Campos EXACTOS de la tabla SQL
    """
    # Campos EXACTOS
    idexperiencilaboral = models.AutoField(primary_key=True, db_column='idexperiencilaboral')
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='experiencias_laborales',
        db_column='idperfilconqueestaactivo'
    )
    cargodesempenado = models.CharField(max_length=100, db_column='cargodesempenado')
    nombrempresa = models.CharField(max_length=50, db_column='nombrempresa')
    lugarempresa = models.CharField(max_length=50, db_column='lugarempresa')
    emailempresa = models.CharField(max_length=100, blank=True, db_column='emailempresa')
    sitiowebempresa = models.CharField(max_length=100, blank=True, db_column='sitiowebempresa')
    nombrecontactoempresarial = models.CharField(max_length=100, blank=True, db_column='nombrecontactoempresarial')
    telefonocontactoempresarial = models.CharField(max_length=60, blank=True, db_column='telefonocontactoempresarial')
    fechainiciogestion = models.DateField(db_column='fechainiciogestion', validators=[validar_fecha_pasada])
    fechafingestion = models.DateField(null=True, blank=True, db_column='fechafingestion')
    descripcionfunciones = models.CharField(max_length=100, db_column='descripcionfunciones')
    activarparaqueseveaenfront = models.BooleanField(default=True, db_column='activarparaqueseveaenfront')
    rutacertificado = models.CharField(max_length=100, blank=True, db_column='rutacertificado')
    
    # Campo adicional para subir archivos
    archivo_certificado = models.FileField(
        upload_to='certificados/experiencia/',
        blank=True,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    
    class Meta:
        db_table = 'experiencialaboral'
        verbose_name = 'Experiencia Laboral'
        verbose_name_plural = 'Experiencias Laborales'
        ordering = ['-fechainiciogestion']
    
    def __str__(self):
        return f"{self.cargodesempenado} - {self.nombrempresa}"
    
    def clean(self):
        if self.fechafingestion:
            if self.fechafingestion > date.today():
                raise ValidationError({'fechafingestion': 'La fecha de fin no puede ser futura'})
            if self.fechafingestion < self.fechainiciogestion:
                raise ValidationError({'fechafingestion': 'La fecha de fin no puede ser anterior a la fecha de inicio'})


# ======================================
# TABLA: RECONOCIMIENTOS
# ======================================

class Reconocimiento(models.Model):
    """
    Mapea: RECONOCIMIENTOS
    Campos EXACTOS de la tabla SQL
    """
    TIPO_CHOICES = [
        ('Académico', 'Académico'),
        ('Público', 'Público'),
        ('Privado', 'Privado'),
    ]
    
    # Campos EXACTOS
    idreconocimiento = models.AutoField(primary_key=True, db_column='idreconocimiento')
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='reconocimientos',
        db_column='idperfilconqueestaactivo'
    )
    tiporeconocimiento = models.CharField(max_length=100, choices=TIPO_CHOICES, db_column='tiporeconocimiento')
    fechareconocimiento = models.DateField(db_column='fechareconocimiento', validators=[validar_fecha_pasada])
    descripcionreconocimiento = models.CharField(max_length=100, db_column='descripcionreconocimiento')
    entidadpatrocinadora = models.CharField(max_length=100, db_column='entidadpatrocinadora')
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, db_column='nombrecontactoauspicia')
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True, db_column='telefonocontactoauspicia')
    activarparaqueseveaenfront = models.BooleanField(default=True, db_column='activarparaqueseveaenfront')
    rutacertificado = models.CharField(max_length=100, blank=True, db_column='rutacertificado')
    
    # Campo adicional
    archivo_certificado = models.FileField(
        upload_to='certificados/reconocimientos/',
        blank=True,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    
    class Meta:
        db_table = 'reconocimientos'
        verbose_name = 'Reconocimiento'
        verbose_name_plural = 'Reconocimientos'
        ordering = ['-fechareconocimiento']
    
    def __str__(self):
        return f"{self.tiporeconocimiento} - {self.entidadpatrocinadora}"
    
    def clean(self):
        if self.fechareconocimiento > date.today():
            raise ValidationError({'fechareconocimiento': 'La fecha no puede ser futura'})


# ======================================
# TABLA: CURSOSREALIZADOS
# ======================================

class CursoRealizado(models.Model):
    """
    Mapea: CURSOSREALIZADOS
    Campos EXACTOS de la tabla SQL
    """
    # Campos EXACTOS
    idcursorealizado = models.AutoField(primary_key=True, db_column='idcursorealizado')
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='cursos_realizados',
        db_column='idperfilconqueestaactivo'
    )
    nombrecurso = models.CharField(max_length=100, db_column='nombrecurso')
    fechainicio = models.DateField(db_column='fechainicio', validators=[validar_fecha_pasada])
    fechafin = models.DateField(db_column='fechafin')
    totalhoras = models.IntegerField(db_column='totalhoras')
    descripcioncurso = models.CharField(max_length=100, db_column='descripcioncurso')
    entidadpatrocinadora = models.CharField(max_length=100, db_column='entidadpatrocinadora')
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, db_column='nombrecontactoauspicia')
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True, db_column='telefonocontactoauspicia')
    emailempresapatrocinadora = models.CharField(max_length=60, blank=True, db_column='emailempresapatrocinadora')
    activarparaqueseveaenfront = models.BooleanField(default=True, db_column='activarparaqueseveaenfront')
    rutacertificado = models.CharField(max_length=100, blank=True, db_column='rutacertificado')
    
    # Campo adicional
    archivo_certificado = models.FileField(
        upload_to='certificados/cursos/',
        blank=True,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    
    class Meta:
        db_table = 'cursosrealizados'
        verbose_name = 'Curso Realizado'
        verbose_name_plural = 'Cursos Realizados'
        ordering = ['-fechainicio']
    
    def __str__(self):
        return f"{self.nombrecurso} - {self.entidadpatrocinadora}"
    
    def clean(self):
        if self.fechafin > date.today():
            raise ValidationError({'fechafin': 'La fecha de fin no puede ser futura'})
        if self.fechainicio and self.fechafin < self.fechainicio:
            raise ValidationError({'fechafin': 'La fecha de fin no puede ser anterior a la fecha de inicio'})


# ======================================
# TABLA: PRODUCTOSACADEMICOS
# ======================================

class ProductoAcademico(models.Model):
    """
    Mapea: PRODUCTOSACADEMICOS
    Campos EXACTOS de la tabla SQL
    """
    # Campos EXACTOS
    idproductoacademico = models.AutoField(primary_key=True, db_column='idproductoacademico')
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='productos_academicos',
        db_column='idperfilconqueestaactivo'
    )
    nombrerecurso = models.CharField(max_length=100, db_column='nombrerecurso')
    clasificador = models.CharField(max_length=100, db_column='clasificador')
    descripcion = models.CharField(max_length=100, db_column='descripcion')
    activarparaqueseveaenfront = models.BooleanField(default=True, db_column='activarparaqueseveaenfront')
    
    class Meta:
        db_table = 'productosacademicos'
        verbose_name = 'Producto Académico'
        verbose_name_plural = 'Productos Académicos'
    
    def __str__(self):
        return self.nombrerecurso
    
    def get_etiquetas(self):
        """Devuelve lista de etiquetas del clasificador"""
        return [tag.strip() for tag in self.clasificador.split(',') if tag.strip()]


# ======================================
# TABLA: PRODUCTOSLABORALES
# ======================================

class ProductoLaboral(models.Model):
    """
    Mapea: PRODUCTOSLABORALES
    Campos EXACTOS de la tabla SQL
    """
    # Campos EXACTOS
    idproductoslaborales = models.AutoField(primary_key=True, db_column='idproductoslaborales')
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='productos_laborales',
        db_column='idperfilconqueestaactivo'
    )
    nombreproducto = models.CharField(max_length=100, db_column='nombreproducto')
    fechaproducto = models.DateField(db_column='fechaproducto', validators=[validar_fecha_pasada])
    descripcion = models.CharField(max_length=100, db_column='descripcion')
    activarparaqueseveaenfront = models.BooleanField(default=True, db_column='activarparaqueseveaenfront')
    
    class Meta:
        db_table = 'productoslaborales'
        verbose_name = 'Producto Laboral'
        verbose_name_plural = 'Productos Laborales'
        ordering = ['-fechaproducto']
    
    def __str__(self):
        return self.nombreproducto


# ======================================
# TABLA: VENTAGARAGE
# ======================================

class VentaGarage(models.Model):
    """
    Mapea: VENTAGARAGE
    Campos EXACTOS de la tabla SQL
    """
    ESTADO_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]
    
    # Campos EXACTOS
    idventagarage = models.AutoField(primary_key=True, db_column='idventagarage')
    idperfilconqueestaactivo = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        related_name='ventas_garage',
        db_column='idperfilconqueestaactivo'
    )
    nombreproducto = models.CharField(max_length=100, db_column='nombreproducto')
    estadoproducto = models.CharField(max_length=40, choices=ESTADO_CHOICES, db_column='estadoproducto')
    descripcion = models.CharField(max_length=100, db_column='descripcion')
    valordelbien = models.DecimalField(max_digits=5, decimal_places=2, db_column='valordelbien')
    activarparaqueseveaenfront = models.BooleanField(default=True, db_column='activarparaqueseveaenfront')
    
    # Campos adicionales (corrección del profesor)
    fecha_publicacion = models.DateField(default=date.today)
    imagen_producto = models.ImageField(upload_to='venta_garage/', blank=True, null=True)
    
    class Meta:
        db_table = 'ventagarage'
        verbose_name = 'Venta Garage'
        verbose_name_plural = 'Ventas Garage'
        ordering = ['-fecha_publicacion']
    
    def __str__(self):
        return f"{self.nombreproducto} - ${self.valordelbien}"
    
    def get_color_estado(self):
        """Color según estado"""
        return '#28a745' if self.estadoproducto == 'Bueno' else '#ffc107'
