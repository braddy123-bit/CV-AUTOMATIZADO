"""
Configuración de la aplicación Curriculum
"""

from django.apps import AppConfig


class CurriculumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'curriculum'
    verbose_name = 'Curriculum Vitae Profesional'
    
    def ready(self):
        """
        Importar signals cuando la app está lista
        """
        try:
            import curriculum.signals
        except ImportError:
            pass
