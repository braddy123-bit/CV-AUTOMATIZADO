"""
Configuración del Panel de Administración
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    PerfilProfesional,
    FormacionAcademica,
    ExperienciaProfesional,
    Habilidad,
    Proyecto,
    ReferenciaProfesional,
    Certificacion
)


# ======================================
# INLINE ADMIN
# ======================================

class FormacionAcademicaInline(admin.TabularInline):
    model = FormacionAcademica
    extra = 0
    fields = ['nivel', 'titulo_obtenido', 'institucion', 'fecha_inicio', 'fecha_fin', 'estado']
    readonly_fields = []


class ExperienciaProfesionalInline(admin.TabularInline):
    model = ExperienciaProfesional
    extra = 0
    fields = ['cargo', 'empresa', 'fecha_inicio', 'fecha_fin', 'trabajo_actual']
    readonly_fields = []


class HabilidadInline(admin.TabularInline):
    model = Habilidad
    extra = 0
    fields = ['nombre', 'tipo', 'nivel', 'destacada']
    readonly_fields = []


class ProyectoInline(admin.StackedInline):
    model = Proyecto
    extra = 0
    fields = ['nombre', 'descripcion_corta', 'estado', 'destacado']
    readonly_fields = []


# ======================================
# PERFIL PROFESIONAL ADMIN
# ======================================

@admin.register(PerfilProfesional)
class PerfilProfesionalAdmin(admin.ModelAdmin):
    list_display = [
        'foto_preview',
        'nombre_completo',
        'usuario',
        'email',
        'titulo_profesional',
        'cv_publico_badge',
        'fecha_actualizacion'
    ]
    
    list_filter = [
        'cv_publico',
        'nivel_experiencia',
        'fecha_creacion',
        'pais',
        'provincia'
    ]
    
    search_fields = [
        'nombres',
        'apellidos',
        'email',
        'titulo_profesional',
        'usuario__username'
    ]
    
    readonly_fields = [
        'slug',
        'fecha_creacion',
        'fecha_actualizacion',
        'foto_preview_large',
        'ver_cv_publico'
    ]
    
    fieldsets = (
        ('Usuario', {
            'fields': ('usuario',)
        }),
        ('Información Personal', {
            'fields': (
                'nombres',
                'apellidos',
                'fecha_nacimiento',
                'nacionalidad',
                'foto',
                'foto_preview_large'
            )
        }),
        ('Contacto', {
            'fields': (
                'email',
                'telefono',
                'linkedin',
                'github',
                'portafolio_web'
            )
        }),
        ('Ubicación', {
            'fields': ('ciudad', 'provincia', 'pais')
        }),
        ('Profesional', {
            'fields': (
                'titulo_profesional',
                'nivel_experiencia',
                'anos_experiencia',
                'resumen_profesional',
                'objetivo_profesional'
            )
        }),
        ('Configuración', {
            'fields': (
                'cv_publico',
                'slug',
                'ver_cv_publico'
            )
        }),
        ('Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        FormacionAcademicaInline,
        ExperienciaProfesionalInline,
        HabilidadInline,
        ProyectoInline
    ]
    
    def foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.foto.url
            )
        return format_html('<div style="width: 50px; height: 50px; background: #ddd; border-radius: 50%;"></div>')
    
    foto_preview.short_description = 'Foto'
    
    def foto_preview_large(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="200" height="200" style="border-radius: 10px; object-fit: cover;" />',
                obj.foto.url
            )
        return 'Sin foto'
    
    foto_preview_large.short_description = 'Vista previa'
    
    def cv_publico_badge(self, obj):
        if obj.cv_publico:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">✓ Público</span>'
            )
        return format_html(
            '<span style="background: #6c757d; color: white; padding: 3px 8px; border-radius: 3px;">✗ Privado</span>'
        )
    
    cv_publico_badge.short_description = 'Visibilidad'
    
    def ver_cv_publico(self, obj):
        if obj.cv_publico:
            url = reverse('curriculum:cv_publico', kwargs={'slug': obj.slug})
            return format_html(
                '<a href="{}" target="_blank" class="button">Ver CV Público →</a>',
                url
            )
        return 'CV no es público'
    
    ver_cv_publico.short_description = 'CV Público'


# ======================================
# FORMACIÓN ACADÉMICA ADMIN
# ======================================

@admin.register(FormacionAcademica)
class FormacionAcademicaAdmin(admin.ModelAdmin):
    list_display = [
        'titulo_obtenido',
        'institucion',
        'nivel',
        'estado',
        'fecha_inicio',
        'fecha_fin',
        'perfil'
    ]
    
    list_filter = ['nivel', 'estado', 'fecha_inicio']
    search_fields = ['titulo_obtenido', 'institucion', 'perfil__nombres', 'perfil__apellidos']
    
    fieldsets = (
        ('Información Académica', {
            'fields': (
                'perfil',
                'nivel',
                'titulo_obtenido',
                'institucion'
            )
        }),
        ('Fechas', {
            'fields': (
                'fecha_inicio',
                'fecha_fin',
                'estado'
            )
        }),
        ('Detalles', {
            'fields': (
                'promedio',
                'descripcion',
                'certificado'
            )
        }),
        ('Configuración', {
            'fields': ('orden',)
        }),
    )


# ======================================
# EXPERIENCIA PROFESIONAL ADMIN
# ======================================

@admin.register(ExperienciaProfesional)
class ExperienciaProfesionalAdmin(admin.ModelAdmin):
    list_display = [
        'cargo',
        'empresa',
        'tipo_empleo',
        'fecha_inicio',
        'fecha_fin',
        'trabajo_actual_badge',
        'perfil'
    ]
    
    list_filter = ['tipo_empleo', 'trabajo_actual', 'pais', 'fecha_inicio']
    search_fields = ['cargo', 'empresa', 'perfil__nombres', 'perfil__apellidos']
    
    fieldsets = (
        ('Información Laboral', {
            'fields': (
                'perfil',
                'cargo',
                'empresa',
                'tipo_empleo'
            )
        }),
        ('Ubicación', {
            'fields': ('ciudad', 'pais')
        }),
        ('Fechas', {
            'fields': (
                'fecha_inicio',
                'fecha_fin',
                'trabajo_actual'
            )
        }),
        ('Descripción', {
            'fields': (
                'descripcion',
                'logros',
                'tecnologias_usadas'
            )
        }),
        ('Configuración', {
            'fields': ('orden',)
        }),
    )
    
    def trabajo_actual_badge(self, obj):
        if obj.trabajo_actual:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">Actual</span>'
            )
        return '-'
    
    trabajo_actual_badge.short_description = 'Estado'


# ======================================
# HABILIDADES ADMIN
# ======================================

@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'tipo',
        'nivel_barra',
        'anos_experiencia',
        'destacada_badge',
        'perfil'
    ]
    
    list_filter = ['tipo', 'destacada', 'nivel']
    search_fields = ['nombre', 'perfil__nombres', 'perfil__apellidos']
    
    fieldsets = (
        ('Información', {
            'fields': (
                'perfil',
                'nombre',
                'tipo'
            )
        }),
        ('Nivel', {
            'fields': (
                'nivel',
                'anos_experiencia',
                'descripcion'
            )
        }),
        ('Certificación', {
            'fields': ('certificado',)
        }),
        ('Configuración', {
            'fields': ('orden', 'destacada')
        }),
    )
    
    def nivel_barra(self, obj):
        porcentaje = obj.nivel
        color = '#28a745' if porcentaje >= 75 else '#ffc107' if porcentaje >= 50 else '#dc3545'
        return format_html(
            '<div style="width: 150px; background: #e9ecef; border-radius: 5px; overflow: hidden;">'
            '<div style="width: {}%; background: {}; color: white; text-align: center; padding: 2px 0; font-size: 11px;">{} %</div>'
            '</div>',
            porcentaje, color, porcentaje
        )
    
    nivel_barra.short_description = 'Nivel'
    
    def destacada_badge(self, obj):
        if obj.destacada:
            return format_html('<span style="color: gold; font-size: 16px;">★</span>')
        return '-'
    
    destacada_badge.short_description = 'Destacada'


# ======================================
# PROYECTOS ADMIN
# ======================================

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = [
        'imagen_preview',
        'nombre',
        'estado',
        'fecha_inicio',
        'destacado_badge',
        'perfil'
    ]
    
    list_filter = ['estado', 'destacado', 'fecha_inicio']
    search_fields = ['nombre', 'descripcion_corta', 'perfil__nombres']
    
    readonly_fields = ['imagen_preview_large']
    
    fieldsets = (
        ('Información del Proyecto', {
            'fields': (
                'perfil',
                'nombre',
                'descripcion_corta',
                'descripcion',
                'estado'
            )
        }),
        ('Fechas y Rol', {
            'fields': (
                'fecha_inicio',
                'fecha_fin',
                'rol',
                'tecnologias'
            )
        }),
        ('Enlaces', {
            'fields': (
                'url_demo',
                'url_repositorio'
            )
        }),
        ('Imagen', {
            'fields': (
                'imagen',
                'imagen_preview_large'
            )
        }),
        ('Configuración', {
            'fields': ('orden', 'destacado')
        }),
    )
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="80" height="45" style="border-radius: 5px; object-fit: cover;" />',
                obj.imagen.url
            )
        return '-'
    
    imagen_preview.short_description = 'Imagen'
    
    def imagen_preview_large(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="400" height="225" style="border-radius: 10px; object-fit: cover;" />',
                obj.imagen.url
            )
        return 'Sin imagen'
    
    imagen_preview_large.short_description = 'Vista previa'
    
    def destacado_badge(self, obj):
        if obj.destacado:
            return format_html('<span style="color: gold; font-size: 16px;">★</span>')
        return '-'
    
    destacado_badge.short_description = 'Destacado'


# ======================================
# REFERENCIAS ADMIN
# ======================================

@admin.register(ReferenciaProfesional)
class ReferenciaProfesionalAdmin(admin.ModelAdmin):
    list_display = [
        'nombre_completo',
        'cargo',
        'empresa',
        'email',
        'mostrar_contacto_badge',
        'perfil'
    ]
    
    search_fields = ['nombre_completo', 'cargo', 'empresa', 'perfil__nombres']
    list_filter = ['mostrar_contacto']
    
    fieldsets = (
        ('Información de la Referencia', {
            'fields': (
                'perfil',
                'nombre_completo',
                'cargo',
                'empresa',
                'relacion'
            )
        }),
        ('Contacto', {
            'fields': (
                'email',
                'telefono',
                'linkedin'
            )
        }),
        ('Testimonio', {
            'fields': ('testimonio',)
        }),
        ('Configuración', {
            'fields': ('orden', 'mostrar_contacto')
        }),
    )
    
    def mostrar_contacto_badge(self, obj):
        if obj.mostrar_contacto:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    
    mostrar_contacto_badge.short_description = 'Mostrar contacto'


# ======================================
# CERTIFICACIONES ADMIN
# ======================================

@admin.register(Certificacion)
class CertificacionAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'institucion',
        'fecha_obtencion',
        'vigencia_badge',
        'perfil'
    ]
    
    list_filter = ['fecha_obtencion', 'institucion']
    search_fields = ['nombre', 'institucion', 'perfil__nombres']
    
    fieldsets = (
        ('Información de la Certificación', {
            'fields': (
                'perfil',
                'nombre',
                'institucion'
            )
        }),
        ('Fechas', {
            'fields': (
                'fecha_obtencion',
                'fecha_expiracion'
            )
        }),
        ('Credenciales', {
            'fields': (
                'codigo_credencial',
                'url_verificacion'
            )
        }),
        ('Detalles', {
            'fields': (
                'descripcion',
                'certificado'
            )
        }),
        ('Configuración', {
            'fields': ('orden',)
        }),
    )
    
    def vigencia_badge(self, obj):
        if obj.esta_vigente:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">Vigente</span>'
            )
        return format_html(
            '<span style="background: #dc3545; color: white; padding: 3px 8px; border-radius: 3px;">Expirado</span>'
        )
    
    vigencia_badge.short_description = 'Estado'
