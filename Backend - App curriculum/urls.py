"""
URLs del módulo curriculum
"""

from django.urls import path
from . import views

app_name = 'curriculum'

urlpatterns = [
    # ======================================
    # PÚBLICAS
    # ======================================
    path('', views.HomeView.as_view(), name='home'),
    path('cv/<slug:slug>/', views.CVPublicoView.as_view(), name='cv_publico'),
    
    # ======================================
    # AUTENTICACIÓN
    # ======================================
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # ======================================
    # DASHBOARD
    # ======================================
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('mi-cv/', views.VerCVView.as_view(), name='ver_cv'),
    
    # ======================================
    # PERFIL PROFESIONAL
    # ======================================
    path('perfil/crear/', views.CrearPerfilView.as_view(), name='crear_perfil'),
    path('perfil/editar/', views.EditarPerfilView.as_view(), name='editar_perfil'),
    
    # ======================================
    # FORMACIÓN ACADÉMICA
    # ======================================
    path('educacion/crear/', views.CrearFormacionView.as_view(), name='crear_educacion'),
    path('educacion/<int:pk>/editar/', views.EditarFormacionView.as_view(), name='editar_educacion'),
    path('educacion/<int:pk>/eliminar/', views.EliminarFormacionView.as_view(), name='eliminar_educacion'),
    
    # ======================================
    # EXPERIENCIA PROFESIONAL
    # ======================================
    path('experiencia/crear/', views.CrearExperienciaView.as_view(), name='crear_experiencia'),
    path('experiencia/<int:pk>/editar/', views.EditarExperienciaView.as_view(), name='editar_experiencia'),
    path('experiencia/<int:pk>/eliminar/', views.EliminarExperienciaView.as_view(), name='eliminar_experiencia'),
    
    # ======================================
    # HABILIDADES
    # ======================================
    path('habilidad/crear/', views.CrearHabilidadView.as_view(), name='crear_habilidad'),
    path('habilidad/<int:pk>/editar/', views.EditarHabilidadView.as_view(), name='editar_habilidad'),
    path('habilidad/<int:pk>/eliminar/', views.EliminarHabilidadView.as_view(), name='eliminar_habilidad'),
    
    # ======================================
    # PROYECTOS
    # ======================================
    path('proyecto/crear/', views.CrearProyectoView.as_view(), name='crear_proyecto'),
    path('proyecto/<int:pk>/editar/', views.EditarProyectoView.as_view(), name='editar_proyecto'),
    path('proyecto/<int:pk>/eliminar/', views.EliminarProyectoView.as_view(), name='eliminar_proyecto'),
    
    # ======================================
    # REFERENCIAS PROFESIONALES
    # ======================================
    path('referencia/crear/', views.CrearReferenciaView.as_view(), name='crear_referencia'),
    path('referencia/<int:pk>/editar/', views.EditarReferenciaView.as_view(), name='editar_referencia'),
    path('referencia/<int:pk>/eliminar/', views.EliminarReferenciaView.as_view(), name='eliminar_referencia'),
    
    # ======================================
    # CERTIFICACIONES
    # ======================================
    path('certificacion/crear/', views.CrearCertificacionView.as_view(), name='crear_certificacion'),
    path('certificacion/<int:pk>/editar/', views.EditarCertificacionView.as_view(), name='editar_certificacion'),
    path('certificacion/<int:pk>/eliminar/', views.EliminarCertificacionView.as_view(), name='eliminar_certificacion'),
    
    # ======================================
    # GENERACIÓN DE PDF
    # ======================================
    path('descargar-cv/', views.descargar_cv_pdf, name='descargar_cv'),
    path('visualizar-cv/', views.visualizar_cv_pdf, name='visualizar_cv'),
]
