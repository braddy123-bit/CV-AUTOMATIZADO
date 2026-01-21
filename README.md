# Hoja-de-vida-Braddy-Vera-Anchundia
# 📄 CV Profesional - Sistema de Gestión de Currículum Vitae


## 🚀 Características Principales

### ✨ Completamente Automatizado
- *Procesamiento automático de imágenes* con ImageKit (redimensionamiento y optimización)
- *Generación automática de slugs* para CVs públicos con UUID
- *Cálculo automático* de años de experiencia y progreso del CV
- *Validación automática* de formularios con Django + Crispy Forms
- *Limpieza automática* de fechas en trabajos actuales

### 📋 Secciones del CV
1. *Perfil Profesional* - Datos personales, foto, contacto, resumen
2. *Formación Académica* - Títulos, instituciones, promedios, certificados
3. *Experiencia Profesional* - Trabajos, cargos, logros, tecnologías
4. *Habilidades* - Técnicas, blandas, idiomas (con niveles 0-100%)
5. *Proyectos* - Portafolio con imágenes, enlaces demo y repositorios
6. *Certificaciones* - Cursos con códigos de credencial y verificación
7. *Referencias Profesionales* - Contactos con control de privacidad

### 🎨 Diseño Moderno
- *Bootstrap 5.3.2* con diseño personalizado
- *Bootstrap Icons 1.11.3* para iconografía
- *Google Fonts* (Inter + Roboto)
- *Gradientes modernos* y animaciones suaves
- *Completamente responsive* (móvil, tablet, desktop)
- *Dark mode ready* (opcional)

### 📦 Funcionalidades Avanzadas
- ✅ Generación de PDF profesional con ReportLab
- ✅ CVs públicos con URL personalizada
- ✅ Panel administrativo customizado con previews
- ✅ Dashboard con estadísticas y progreso
- ✅ Almacenamiento flexible (local/Azure/S3)
- ✅ Validación de teléfonos internacionales
- ✅ Template tags personalizados
- ✅ Sistema de mensajes con auto-dismiss

---

## 🛠️ Tecnologías Utilizadas

### Backend
- *Django 4.2.9* - Framework principal
- *Python 3.10+* - Lenguaje de programación
- *PostgreSQL/SQLite* - Base de datos
- *ReportLab* - Generación de PDFs
- *Pillow + ImageKit* - Procesamiento de imágenes
- *django-phonenumber-field* - Validación de teléfonos

### Frontend
- *Bootstrap 5.3.2* - Framework CSS
- *Bootstrap Icons* - Iconografía
- *Vanilla JavaScript* - Interactividad
- *Google Fonts* - Tipografías

### Deployment
- *Gunicorn* - Servidor WSGI
- *WhiteNoise* - Archivos estáticos
- *dj-database-url* - Configuración de BD
- *python-decouple* - Variables de entorno

---

## 📥 Instalación

### Requisitos Previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (recomendado)
- Git

### Pasos de Instalación

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/cv-profesional.git
cd cv-profesional
```

#### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### 4. Configurar Variables de Entorno
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores
# - SECRET_KEY
# - DEBUG
# - DATABASE_URL
# - etc.
```

#### 5. Crear Base de Datos
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Crear Superusuario
```bash
python manage.py createsuperuser
```

#### 7. Crear Carpetas de Media
```bash
mkdir -p media/profile_photos
mkdir -p media/certificates/education
mkdir -p media/certificates/skills
mkdir -p media/certificates/certifications
mkdir -p media/project_images
mkdir -p media/documents
```

#### 8. Recolectar Archivos Estáticos (Producción)
```bash
python manage.py collectstatic --no-input
```

#### 9. Iniciar Servidor de Desarrollo
```bash
python manage.py runserver
```

Accede a: **http://localhost:8000**

---

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# Django
SECRET_KEY=tu-secret-key-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3
# PostgreSQL: postgresql://usuario:password@localhost:5432/cv_db

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# Storage
STORAGE_BACKEND=local
# Opciones: local, azure, s3

# Azure (opcional)
AZURE_STORAGE_ACCOUNT_NAME=
AZURE_STORAGE_ACCOUNT_KEY=
AZURE_CONTAINER=media

# AWS S3 (opcional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1

# Features
ENABLE_PDF_DOWNLOAD=True
ENABLE_PUBLIC_CV=True
ENABLE_DARK_MODE=True
ENABLE_REFERENCES=True
```

---

## 📖 Uso

### Para Usuarios

#### 1. Registro
- Ir a http://localhost:8000/registro/
- Completar formulario de registro
- Verificar email (si está configurado)

#### 2. Crear Perfil
- Acceder al dashboard
- Hacer clic en "Crear Perfil"
- Completar datos personales y profesionales

#### 3. Agregar Información
- *Formación Académica*: Dashboard → Agregar formación
- *Experiencia Profesional*: Dashboard → Agregar experiencia
- *Habilidades*: Dashboard → Agregar habilidad
- *Proyectos*: Dashboard → Agregar proyecto
- *Certificaciones*: Dashboard → Agregar certificación
- *Referencias*: Dashboard → Agregar referencia

#### 4. Descargar CV
- Dashboard → "Descargar CV en PDF"
- O ver CV → "Descargar PDF"

#### 5. Compartir CV Público
- Editar perfil → Marcar "CV Público"
- Compartir URL: http://localhost:8000/cv/tu-slug/

### Para Administradores

#### 1. Acceder al Admin
http://localhost:8000/admin/

#### 2. Gestionar Usuarios
- Ver todos los perfiles
- Editar información de usuarios
- Activar/desactivar cuentas

#### 3. Estadísticas
- Total de usuarios
- CVs públicos
- Usuarios activos

---

## 📁 Estructura del Proyecto

```
cv_profesional/
├── cv_profesional/          # Configuración del proyecto
│   ├── settings.py          # Configuración principal
│   ├── urls.py              # URLs principales
│   ├── wsgi.py              # WSGI config
│   └── asgi.py              # ASGI config
│
├── curriculum/              # App principal
│   ├── models.py            # 7 modelos (Perfil, Experiencia, etc.)
│   ├── forms.py             # 9 formularios con Crispy
│   ├── views.py             # Vistas class-based
│   ├── urls.py              # URLs de la app
│   ├── admin.py             # Admin personalizado
│   ├── pdf_generator.py     # Generador de PDF
│   ├── utils.py             # Funciones auxiliares
│   ├── storage_backends.py  # Azure Storage
│   │
│   ├── templates/           # Templates HTML
│   │   └── curriculum/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── auth/        # Login, registro
│   │       ├── cv/          # Dashboard, vista CV
│   │       ├── sections/    # Formularios
│   │       ├── components/  # Navbar, footer, messages
│   │       └── errors/      # 404, 500, 403
│   │
│   ├── static/              # Archivos estáticos
│   │   └── curriculum/
│   │       ├── css/         # main.css, forms.css, cv.css
│   │       ├── js/          # main.js, forms.js
│   │       └── img/         # Imágenes
│   │
│   └── templatetags/        # Tags personalizados
│       └── cv_filters.py
│
├── media/                   # Archivos subidos
├── staticfiles/             # Estáticos recolectados
├── requirements.txt         # Dependencias
├── .env.example             # Ejemplo de variables
├── .gitignore               # Archivos ignorados
├── manage.py                # Script de Django
└── README.md                # Esta documentación
```

---

## 🎯 Modelos de Datos

### PerfilProfesional
- Información personal y profesional
- Foto procesada automáticamente
- Contacto (email, teléfono, redes)
- Ubicación, resumen, objetivo

### FormacionAcademica
- Nivel educativo (bachillerato a doctorado)
- Institución, título, fechas
- Promedio, certificado PDF

### ExperienciaProfesional
- Cargo, empresa, tipo de empleo
- Fechas, trabajo actual
- Descripción, logros, tecnologías

### Habilidad
- Nombre, tipo (técnica/blanda/idioma)
- Nivel 0-100%, años experiencia
- Certificado opcional

### Proyecto
- Nombre, descripción, estado
- Imagen procesada
- URLs (demo, repo)
- Destacado

### Certificacion
- Nombre, institución
- Fechas, código credencial
- URL verificación

### ReferenciaProfesional
- Datos del referente
- Relación profesional
- Control de privacidad

---

## 🚀 Deployment

### Render.com

1. Crear cuenta en Render
2. Conectar repositorio de GitHub
3. Configurar variables de entorno
4. Deploy automático

### Heroku

```bash
heroku create cv-profesional
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Railway

1. Conectar repositorio
2. Configurar variables
3. Deploy automático

---

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Con coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

## 👤 Autor

*Braddy Londre Vera Anchundia*
- GitHub: [@braddy123-bit](https://github.com/braddy123-bit)
- Email: braddylondre123@gmail.com

---

## 🔄 Changelog

### v1.0.0 (2026-01-20)
- ✨ Lanzamiento inicial
- ✅ 7 modelos completos
- ✅ Sistema de autenticación
- ✅ Dashboard con estadísticas
- ✅ Generación de PDF
- ✅ Admin personalizado
- ✅ Diseño responsive
- ✅ Storage flexible
