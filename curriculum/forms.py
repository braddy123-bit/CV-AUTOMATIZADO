"""
Formularios para el Sistema de CV Profesional
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from crispy_forms.bootstrap import PrependedText, AppendedText
from .models import (
    PerfilProfesional, 
    FormacionAcademica, 
    ExperienciaProfesional,
    Habilidad,
    Proyecto,
    ReferenciaProfesional,
    Certificacion
)
import re


# ======================================
# FORMULARIOS DE AUTENTICACIÓN
# ======================================

class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario de registro mejorado
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )
    
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label='Nombres',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Juan'
        })
    )
    
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label='Apellidos',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pérez'
        })
    )
    
    aceptar_terminos = forms.BooleanField(
        required=True,
        label='Acepto los términos y condiciones'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'usuario123'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('username', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-3'),
                Column('password2', css_class='form-group col-md-6 mb-3'),
            ),
            'aceptar_terminos',
            Submit('submit', 'Crear Cuenta', css_class='btn btn-primary btn-lg w-100 mt-3')
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email ya está registrado.')
        return email


class LoginForm(AuthenticationForm):
    """
    Formulario de login mejorado
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        label='Recordarme'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            'remember_me',
            Submit('submit', 'Iniciar Sesión', css_class='btn btn-primary btn-lg w-100 mt-3')
        )


# ======================================
# FORMULARIO: PERFIL PROFESIONAL
# ======================================

class PerfilProfesionalForm(forms.ModelForm):
    """
    Formulario para crear/editar perfil profesional
    """
    class Meta:
        model = PerfilProfesional
        fields = [
            'nombres', 'apellidos', 'fecha_nacimiento', 'nacionalidad',
            'foto', 'email', 'telefono', 'linkedin', 'github', 'portafolio_web',
            'ciudad', 'provincia', 'pais',
            'titulo_profesional', 'nivel_experiencia', 'anos_experiencia',
            'resumen_profesional', 'objetivo_profesional',
            'cv_publico'
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Carlos'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pérez González'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ecuatoriana'}),
            'foto': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@profesional.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+593 99 123 4567'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/tu-perfil'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/tu-usuario'}),
            'portafolio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://tu-portafolio.com'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quito'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pichincha'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ecuador'}),
            'titulo_profesional': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Desarrollador Full Stack'}),
            'nivel_experiencia': forms.Select(attrs={'class': 'form-select'}),
            'anos_experiencia': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 50}),
            'resumen_profesional': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Escribe un resumen breve de tu trayectoria profesional (máx 500 caracteres)'
            }),
            'objetivo_profesional': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Describe tus objetivos profesionales (opcional)'
            }),
            'cv_publico': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h4 class="mb-3"><i class="bi bi-person-circle"></i> Información Personal</h4>'),
            Row(
                Column('nombres', css_class='form-group col-md-6 mb-3'),
                Column('apellidos', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('fecha_nacimiento', css_class='form-group col-md-4 mb-3'),
                Column('nacionalidad', css_class='form-group col-md-8 mb-3'),
            ),
            'foto',
            
            HTML('<h4 class="mb-3 mt-4"><i class="bi bi-telephone"></i> Información de Contacto</h4>'),
            Row(
                Column('email', css_class='form-group col-md-6 mb-3'),
                Column('telefono', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('linkedin', css_class='form-group col-md-4 mb-3'),
                Column('github', css_class='form-group col-md-4 mb-3'),
                Column('portafolio_web', css_class='form-group col-md-4 mb-3'),
            ),
            
            HTML('<h4 class="mb-3 mt-4"><i class="bi bi-geo-alt"></i> Ubicación</h4>'),
            Row(
                Column('ciudad', css_class='form-group col-md-4 mb-3'),
                Column('provincia', css_class='form-group col-md-4 mb-3'),
                Column('pais', css_class='form-group col-md-4 mb-3'),
            ),
            
            HTML('<h4 class="mb-3 mt-4"><i class="bi bi-briefcase"></i> Información Profesional</h4>'),
            'titulo_profesional',
            Row(
                Column('nivel_experiencia', css_class='form-group col-md-6 mb-3'),
                Column('anos_experiencia', css_class='form-group col-md-6 mb-3'),
            ),
            'resumen_profesional',
            'objetivo_profesional',
            
            HTML('<h4 class="mb-3 mt-4"><i class="bi bi-shield-check"></i> Privacidad</h4>'),
            Div('cv_publico', css_class='form-check mb-3'),
            
            Submit('submit', 'Guardar Perfil', css_class='btn btn-primary btn-lg w-100 mt-4')
        )
    
    def clean_resumen_profesional(self):
        resumen = self.cleaned_data.get('resumen_profesional')
        if len(resumen) < 50:
            raise ValidationError('El resumen debe tener al menos 50 caracteres.')
        return resumen
    
    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto:
            if foto.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('La imagen no puede superar 5MB.')
        return foto


# ======================================
# FORMULARIO: FORMACIÓN ACADÉMICA
# ======================================

class FormacionAcademicaForm(forms.ModelForm):
    """
    Formulario para educación
    """
    class Meta:
        model = FormacionAcademica
        fields = [
            'nivel', 'titulo_obtenido', 'institucion',
            'fecha_inicio', 'fecha_fin', 'estado',
            'promedio', 'descripcion', 'certificado'
        ]
        widgets = {
            'nivel': forms.Select(attrs={'class': 'form-select'}),
            'titulo_obtenido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ingeniería en Sistemas'}),
            'institucion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Universidad Central del Ecuador'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'promedio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '10'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Logros, especialización, tesis, etc.'}),
            'certificado': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise ValidationError('La fecha de finalización no puede ser anterior a la fecha de inicio.')
        
        return cleaned_data


# ======================================
# FORMULARIO: EXPERIENCIA PROFESIONAL
# ======================================

class ExperienciaProfesionalForm(forms.ModelForm):
    """
    Formulario para experiencia laboral
    """
    class Meta:
        model = ExperienciaProfesional
        fields = [
            'cargo', 'empresa', 'tipo_empleo',
            'ciudad', 'pais',
            'fecha_inicio', 'fecha_fin', 'trabajo_actual',
            'descripcion', 'logros', 'tecnologias_usadas'
        ]
        widgets = {
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Desarrollador Full Stack Senior'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Tech Solutions S.A.'}),
            'tipo_empleo': forms.Select(attrs={'class': 'form-select'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guayaquil'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ecuador'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'trabajo_actual': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Describe tus responsabilidades principales...'
            }),
            'logros': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Menciona tus logros cuantificables (Ej: Aumenté las ventas en 30%, Reduje bugs en 40%)'
            }),
            'tecnologias_usadas': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Python, Django, React, PostgreSQL, Docker'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        trabajo_actual = cleaned_data.get('trabajo_actual')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if not trabajo_actual and not fecha_fin:
            raise ValidationError('Debes indicar la fecha de finalización o marcar como trabajo actual.')
        
        return cleaned_data


# ======================================
# FORMULARIO: HABILIDADES
# ======================================

class HabilidadForm(forms.ModelForm):
    """
    Formulario para habilidades
    """
    class Meta:
        model = Habilidad
        fields = ['nombre', 'tipo', 'nivel', 'anos_experiencia', 'descripcion', 'certificado', 'destacada']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Python, Liderazgo, Inglés'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'nivel': forms.NumberInput(attrs={
                'class': 'form-range',
                'min': '0',
                'max': '100',
                'step': '5',
                'oninput': 'this.nextElementSibling.value = this.value'
            }),
            'anos_experiencia': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '50'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'certificado': forms.FileInput(attrs={'class': 'form-control'}),
            'destacada': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


# ======================================
# FORMULARIO: PROYECTOS
# ======================================

class ProyectoForm(forms.ModelForm):
    """
    Formulario para proyectos
    """
    class Meta:
        model = Proyecto
        fields = [
            'nombre', 'descripcion_corta', 'descripcion', 'estado',
            'fecha_inicio', 'fecha_fin', 'rol', 'tecnologias',
            'url_demo', 'url_repositorio', 'imagen', 'destacado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: E-Commerce Platform'}),
            'descripcion_corta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Una línea describiendo el proyecto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Desarrollador Full Stack'}),
            'tecnologias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'React, Node.js, MongoDB'}),
            'url_demo': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://proyecto-demo.com'}),
            'url_repositorio': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/usuario/proyecto'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


# ======================================
# FORMULARIO: REFERENCIAS
# ======================================

class ReferenciaProfesionalForm(forms.ModelForm):
    """
    Formulario para referencias profesionales
    """
    class Meta:
        model = ReferenciaProfesional
        fields = [
            'nombre_completo', 'cargo', 'empresa', 'relacion',
            'email', 'telefono', 'linkedin',
            'testimonio', 'mostrar_contacto'
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'relacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex-supervisor directo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'testimonio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mostrar_contacto': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


# ======================================
# FORMULARIO: CERTIFICACIONES
# ======================================

class CertificacionForm(forms.ModelForm):
    """
    Formulario para certificaciones
    """
    class Meta:
        model = Certificacion
        fields = [
            'nombre', 'institucion', 'fecha_obtencion', 'fecha_expiracion',
            'codigo_credencial', 'url_verificacion', 'descripcion', 'certificado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: AWS Certified Solutions Architect'}),
            'institucion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amazon Web Services'}),
            'fecha_obtencion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_expiracion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'codigo_credencial': forms.TextInput(attrs={'class': 'form-control'}),
            'url_verificacion': forms.URLInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'certificado': forms.FileInput(attrs={'class': 'form-control'})
        }
