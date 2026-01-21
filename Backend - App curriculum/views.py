"""
Vistas para el Sistema de CV Profesional
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.http import HttpResponse, FileResponse, Http404
from django.db.models import Q, Count
from .models import (
    PerfilProfesional,
    FormacionAcademica,
    ExperienciaProfesional,
    Habilidad,
    Proyecto,
    ReferenciaProfesional,
    Certificacion
)
from .forms import (
    RegistroUsuarioForm,
    LoginForm,
    PerfilProfesionalForm,
    FormacionAcademicaForm,
    ExperienciaProfesionalForm,
    HabilidadForm,
    ProyectoForm,
    ReferenciaProfesionalForm,
    CertificacionForm
)
from .pdf_generator import generar_cv_pdf


# ======================================
# VISTAS PÚBLICAS
# ======================================

class HomeView(TemplateView):
    """
    Página principal
    """
    template_name = 'curriculum/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_usuarios'] = PerfilProfesional.objects.count()
        context['cvs_publicos'] = PerfilProfesional.objects.filter(cv_publico=True).count()
        return context


class CVPublicoView(DetailView):
    """
    Ver CV público de un usuario
    """
    model = PerfilProfesional
    template_name = 'curriculum/cv/public_cv.html'
    context_object_name = 'perfil'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return PerfilProfesional.objects.filter(cv_publico=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil = self.object
        
        context['formacion'] = perfil.formacion_academica.all()[:5]
        context['experiencias'] = perfil.experiencias.all()[:10]
        context['habilidades'] = perfil.habilidades.all()[:20]
        context['proyectos'] = perfil.proyectos.filter(destacado=True)[:6]
        context['certificaciones'] = perfil.certificaciones.all()[:10]
        context['referencias'] = perfil.referencias.all()[:3]
        
        return context


# ======================================
# AUTENTICACIÓN
# ======================================

def registro_view(request):
    """
    Registro de nuevos usuarios
    """
    if request.user.is_authenticated:
        return redirect('curriculum:dashboard')
    
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.first_name}! Tu cuenta ha sido creada.')
            return redirect('curriculum:crear_perfil')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'curriculum/auth/register.html', {'form': form})


def login_view(request):
    """
    Login de usuarios
    """
    if request.user.is_authenticated:
        return redirect('curriculum:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Configurar duración de sesión
                if not remember_me:
                    request.session.set_expiry(0)
                
                messages.success(request, f'¡Bienvenido de vuelta, {user.first_name}!')
                
                # Redirigir a la página solicitada o al dashboard
                next_page = request.GET.get('next', 'curriculum:dashboard')
                return redirect(next_page)
    else:
        form = LoginForm()
    
    return render(request, 'curriculum/auth/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Cerrar sesión
    """
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('curriculum:home')


# ======================================
# DASHBOARD
# ======================================

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard principal del usuario
    """
    template_name = 'curriculum/cv/dashboard.html'
    login_url = 'curriculum:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            perfil = self.request.user.perfil
            context['tiene_perfil'] = True
            context['perfil'] = perfil
            
            # Estadísticas
            context['stats'] = {
                'formacion': perfil.formacion_academica.count(),
                'experiencias': perfil.experiencias.count(),
                'habilidades': perfil.habilidades.count(),
                'proyectos': perfil.proyectos.count(),
                'certificaciones': perfil.certificaciones.count(),
                'referencias': perfil.referencias.count(),
            }
            
            # Progreso del CV (porcentaje de completitud)
            total_secciones = 6
            secciones_completas = sum([
                1 if context['stats']['formacion'] > 0 else 0,
                1 if context['stats']['experiencias'] > 0 else 0,
                1 if context['stats']['habilidades'] > 0 else 0,
                1 if context['stats']['proyectos'] > 0 else 0,
                1 if perfil.resumen_profesional else 0,
                1 if perfil.foto else 0,
            ])
            context['progreso'] = int((secciones_completas / total_secciones) * 100)
            
            # Últimas actualizaciones
            context['ultimas_experiencias'] = perfil.experiencias.all()[:3]
            context['ultimos_proyectos'] = perfil.proyectos.all()[:3]
            
        except PerfilProfesional.DoesNotExist:
            context['tiene_perfil'] = False
        
        return context


# ======================================
# PERFIL PROFESIONAL
# ======================================

class CrearPerfilView(LoginRequiredMixin, CreateView):
    """
    Crear perfil profesional
    """
    model = PerfilProfesional
    form_class = PerfilProfesionalForm
    template_name = 'curriculum/sections/perfil_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'perfil'):
            messages.warning(request, 'Ya tienes un perfil creado.')
            return redirect('curriculum:editar_perfil')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, '¡Perfil creado exitosamente!')
        return super().form_valid(form)


class EditarPerfilView(LoginRequiredMixin, UpdateView):
    """
    Editar perfil profesional
    """
    model = PerfilProfesional
    form_class = PerfilProfesionalForm
    template_name = 'curriculum/sections/perfil_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_object(self):
        return self.request.user.perfil
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)


class VerCVView(LoginRequiredMixin, DetailView):
    """
    Ver CV completo del usuario
    """
    model = PerfilProfesional
    template_name = 'curriculum/cv/view_cv.html'
    context_object_name = 'perfil'
    
    def get_object(self):
        return self.request.user.perfil
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil = self.object
        
        context['formacion'] = perfil.formacion_academica.all()
        context['experiencias'] = perfil.experiencias.all()
        context['habilidades'] = perfil.habilidades.all()
        context['proyectos'] = perfil.proyectos.all()
        context['certificaciones'] = perfil.certificaciones.all()
        context['referencias'] = perfil.referencias.all()
        
        return context


# ======================================
# FORMACIÓN ACADÉMICA
# ======================================

class CrearFormacionView(LoginRequiredMixin, CreateView):
    model = FormacionAcademica
    form_class = FormacionAcademicaForm
    template_name = 'curriculum/sections/educacion_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def form_valid(self, form):
        form.instance.perfil = self.request.user.perfil
        messages.success(self.request, 'Formación académica agregada.')
        return super().form_valid(form)


class EditarFormacionView(LoginRequiredMixin, UpdateView):
    model = FormacionAcademica
    form_class = FormacionAcademicaForm
    template_name = 'curriculum/sections/educacion_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return FormacionAcademica.objects.filter(perfil=self.request.user.perfil)
    
    def form_valid(self, form):
        messages.success(self.request, 'Formación académica actualizada.')
        return super().form_valid(form)


class EliminarFormacionView(LoginRequiredMixin, DeleteView):
    model = FormacionAcademica
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return FormacionAcademica.objects.filter(perfil=self.request.user.perfil)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Formación académica eliminada.')
        return super().delete(request, *args, **kwargs)


# ======================================
# EXPERIENCIA PROFESIONAL
# ======================================

class CrearExperienciaView(LoginRequiredMixin, CreateView):
    model = ExperienciaProfesional
    form_class = ExperienciaProfesionalForm
    template_name = 'curriculum/sections/experiencia_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def form_valid(self, form):
        form.instance.perfil = self.request.user.perfil
        messages.success(self.request, 'Experiencia profesional agregada.')
        return super().form_valid(form)


class EditarExperienciaView(LoginRequiredMixin, UpdateView):
    model = ExperienciaProfesional
    form_class = ExperienciaProfesionalForm
    template_name = 'curriculum/sections/experiencia_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return ExperienciaProfesional.objects.filter(perfil=self.request.user.perfil)
    
    def form_valid(self, form):
        messages.success(self.request, 'Experiencia profesional actualizada.')
        return super().form_valid(form)


class EliminarExperienciaView(LoginRequiredMixin, DeleteView):
    model = ExperienciaProfesional
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return ExperienciaProfesional.objects.filter(perfil=self.request.user.perfil)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Experiencia profesional eliminada.')
        return super().delete(request, *args, **kwargs)


# ======================================
# HABILIDADES
# ======================================

class CrearHabilidadView(LoginRequiredMixin, CreateView):
    model = Habilidad
    form_class = HabilidadForm
    template_name = 'curriculum/sections/habilidades_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def form_valid(self, form):
        form.instance.perfil = self.request.user.perfil
        messages.success(self.request, 'Habilidad agregada.')
        return super().form_valid(form)


class EditarHabilidadView(LoginRequiredMixin, UpdateView):
    model = Habilidad
    form_class = HabilidadForm
    template_name = 'curriculum/sections/habilidades_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return Habilidad.objects.filter(perfil=self.request.user.perfil)


class EliminarHabilidadView(LoginRequiredMixin, DeleteView):
    model = Habilidad
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return Habilidad.objects.filter(perfil=self.request.user.perfil)


# ======================================
# PROYECTOS
# ======================================

class CrearProyectoView(LoginRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'curriculum/sections/proyectos_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def form_valid(self, form):
        form.instance.perfil = self.request.user.perfil
        messages.success(self.request, 'Proyecto agregado.')
        return super().form_valid(form)


class EditarProyectoView(LoginRequiredMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'curriculum/sections/proyectos_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return Proyecto.objects.filter(perfil=self.request.user.perfil)


class EliminarProyectoView(LoginRequiredMixin, DeleteView):
    model = Proyecto
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return Proyecto.objects.filter(perfil=self.request.user.perfil)


# ======================================
# REFERENCIAS
# ======================================

class CrearReferenciaView(LoginRequiredMixin, CreateView):
    model = ReferenciaProfesional
    form_class = ReferenciaProfesionalForm
    template_name = 'curriculum/sections/referencias_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def form_valid(self, form):
        form.instance.perfil = self.request.user.perfil
        messages.success(self.request, 'Referencia agregada.')
        return super().form_valid(form)


class EditarReferenciaView(LoginRequiredMixin, UpdateView):
    model = ReferenciaProfesional
    form_class = ReferenciaProfesionalForm
    template_name = 'curriculum/sections/referencias_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return ReferenciaProfesional.objects.filter(perfil=self.request.user.perfil)


class EliminarReferenciaView(LoginRequiredMixin, DeleteView):
    model = ReferenciaProfesional
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return ReferenciaProfesional.objects.filter(perfil=self.request.user.perfil)


# ======================================
# CERTIFICACIONES
# ======================================

class CrearCertificacionView(LoginRequiredMixin, CreateView):
    model = Certificacion
    form_class = CertificacionForm
    template_name = 'curriculum/sections/certificacion_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def form_valid(self, form):
        form.instance.perfil = self.request.user.perfil
        messages.success(self.request, 'Certificación agregada.')
        return super().form_valid(form)


class EditarCertificacionView(LoginRequiredMixin, UpdateView):
    model = Certificacion
    form_class = CertificacionForm
    template_name = 'curriculum/sections/certificacion_form.html'
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return Certificacion.objects.filter(perfil=self.request.user.perfil)


class EliminarCertificacionView(LoginRequiredMixin, DeleteView):
    model = Certificacion
    success_url = reverse_lazy('curriculum:dashboard')
    
    def get_queryset(self):
        return Certificacion.objects.filter(perfil=self.request.user.perfil)


# ======================================
# GENERACIÓN DE PDF
# ======================================

@login_required
def descargar_cv_pdf(request):
    """
    Descargar CV en formato PDF
    """
    try:
        perfil = request.user.perfil
        pdf_buffer = generar_cv_pdf(perfil)
        
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="CV_{perfil.nombre_completo}.pdf"'
        
        return response
    
    except PerfilProfesional.DoesNotExist:
        messages.error(request, 'Debes crear tu perfil primero.')
        return redirect('curriculum:crear_perfil')


@login_required
def visualizar_cv_pdf(request):
    """
    Visualizar CV en el navegador
    """
    try:
        perfil = request.user.perfil
        pdf_buffer = generar_cv_pdf(perfil)
        
        return HttpResponse(pdf_buffer, content_type='application/pdf')
    
    except PerfilProfesional.DoesNotExist:
        messages.error(request, 'Debes crear tu perfil primero.')
        return redirect('curriculum:crear_perfil')


# ======================================
# HANDLERS DE ERRORES
# ======================================

def error_404(request, exception):
    return render(request, 'curriculum/errors/404.html', status=404)


def error_500(request):
    return render(request, 'curriculum/errors/500.html', status=500)


def error_403(request, exception):
    return render(request, 'curriculum/errors/403.html', status=403)
