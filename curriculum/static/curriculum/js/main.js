// ============================================
// CV PROFESIONAL - MAIN JAVASCRIPT
// ============================================

(function() {
    'use strict';

    // ========================================
    // Inicialización al cargar el DOM
    // ========================================
    document.addEventListener('DOMContentLoaded', function() {
        initApp();
    });

    function initApp() {
        initTooltips();
        initPopovers();
        initAlerts();
        initSmoothScroll();
        initAnimations();
        initProgressBars();
        initSkillBars();
        initFormValidation();
    }

    // ========================================
    // Bootstrap Tooltips
    // ========================================
    function initTooltips() {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // ========================================
    // Bootstrap Popovers
    // ========================================
    function initPopovers() {
        const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
        const popoverList = [...popoverTriggerList].map(popoverTriggerEl => {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    // ========================================
    // Auto-dismiss Alerts
    // ========================================
    function initAlerts() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });
    }

    // ========================================
    // Smooth Scroll
    // ========================================
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href !== '#' && href !== '#!') {
                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
    }

    // ========================================
    // Animaciones al hacer scroll
    // ========================================
    function initAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, {
            threshold: 0.1
        });

        document.querySelectorAll('.card, .timeline-item, .project-card').forEach(el => {
            observer.observe(el);
        });
    }

    // ========================================
    // Progress Bars Animadas
    // ========================================
    function initProgressBars() {
        const progressBars = document.querySelectorAll('.progress-bar');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const width = bar.getAttribute('aria-valuenow') || bar.style.width;
                    bar.style.width = '0%';
                    setTimeout(() => {
                        bar.style.transition = 'width 1s ease-in-out';
                        bar.style.width = width.toString().includes('%') ? width : width + '%';
                    }, 100);
                    observer.unobserve(bar);
                }
            });
        }, { threshold: 0.5 });

        progressBars.forEach(bar => observer.observe(bar));
    }

    // ========================================
    // Skill Bars Animadas
    // ========================================
    function initSkillBars() {
        const skillBars = document.querySelectorAll('.skill-level-bar');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const width = bar.getAttribute('data-level') || bar.dataset.width;
                    if (width) {
                        bar.style.width = '0%';
                        setTimeout(() => {
                            bar.style.width = width + '%';
                        }, 100);
                    }
                    observer.unobserve(bar);
                }
            });
        }, { threshold: 0.5 });

        skillBars.forEach(bar => observer.observe(bar));
    }

    // ========================================
    // Validación de Formularios
    // ========================================
    function initFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }

    // ========================================
    // Preview de Imagen (para fotos de perfil)
    // ========================================
    window.previewImage = function(input, targetId) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const target = document.getElementById(targetId);
                if (target) {
                    target.src = e.target.result;
                    target.style.display = 'block';
                }
            };
            reader.readAsDataURL(input.files[0]);
        }
    };

    // ========================================
    // Confirmación de eliminación
    // ========================================
    window.confirmDelete = function(itemName) {
        return confirm(`¿Estás seguro de que deseas eliminar "${itemName}"? Esta acción no se puede deshacer.`);
    };

    // ========================================
    // Copy to Clipboard
    // ========================================
    window.copyToClipboard = function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Copiado al portapapeles', 'success');
            }).catch(err => {
                console.error('Error al copiar:', err);
            });
        }
    };

    // ========================================
    // Notificaciones Toast
    // ========================================
    window.showNotification = function(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            const container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        document.getElementById('toastContainer').appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    };

    // ========================================
    // Contador animado para estadísticas
    // ========================================
    window.animateCounter = function(element, target, duration = 1000) {
        let start = 0;
        const increment = target / (duration / 16);
        
        const timer = setInterval(() => {
            start += increment;
            if (start >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(start);
            }
        }, 16);
    };

    // ========================================
    // Función para cargar contenido dinámico
    // ========================================
    window.loadContent = function(url, targetId) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                document.getElementById(targetId).innerHTML = html;
            })
            .catch(error => {
                console.error('Error cargando contenido:', error);
                showNotification('Error al cargar el contenido', 'danger');
            });
    };

    // ========================================
    // Función para validar URLs
    // ========================================
    window.isValidURL = function(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    };

    // ========================================
    // Función para formatear fechas
    // ========================================
    window.formatDate = function(date, format = 'es-ES') {
        return new Date(date).toLocaleDateString(format, {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    // ========================================
    // Back to Top Button
    // ========================================
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTop.classList.add('show');
            } else {
                backToTop.classList.remove('show');
            }
        });

        backToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ========================================
    // Loading Overlay
    // ========================================
    window.showLoading = function() {
        const overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
        `;
        document.body.appendChild(overlay);
    };

    window.hideLoading = function() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.remove();
        }
    };

    // ========================================
    // Console Welcome Message
    // ========================================
    console.log('%cCV Profesional', 'font-size: 20px; font-weight: bold; color: #2E7D32;');
    console.log('%cSistema de Gestión de Currículum Vitae', 'font-size: 12px; color: #666;');
    console.log('%c© 2026 - Todos los derechos reservados', 'font-size: 10px; color: #999;');

})();

// ========================================
// Export para uso en otros módulos
// ========================================
window.CVApp = {
    showNotification: window.showNotification,
    confirmDelete: window.confirmDelete,
    copyToClipboard: window.copyToClipboard,
    showLoading: window.showLoading,
    hideLoading: window.hideLoading
};
