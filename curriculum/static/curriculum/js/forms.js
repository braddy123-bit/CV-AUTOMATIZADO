// ============================================
// FORMS JAVASCRIPT - Validación y Features
// ============================================

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initFormFeatures();
    });

    function initFormFeatures() {
        handleTrabajoActual();
        handleFileInputs();
        handleRangeInputs();
        handlePhoneInputs();
        handleURLInputs();
        handleCharacterCount();
        handleDateValidation();
    }

    // ========================================
    // Trabajo Actual - Ocultar fecha fin
    // ========================================
    function handleTrabajoActual() {
        const trabajoActualInputs = document.querySelectorAll('input[name="trabajo_actual"]');
        
        trabajoActualInputs.forEach(input => {
            const fechaFinInput = document.querySelector('input[name="fecha_fin"]');
            
            if (fechaFinInput) {
                const fechaFinGroup = fechaFinInput.closest('.form-group, .mb-3');
                
                function toggleFechaFin() {
                    if (input.checked) {
                        fechaFinInput.value = '';
                        fechaFinInput.disabled = true;
                        if (fechaFinGroup) {
                            fechaFinGroup.style.opacity = '0.5';
                        }
                    } else {
                        fechaFinInput.disabled = false;
                        if (fechaFinGroup) {
                            fechaFinGroup.style.opacity = '1';
                        }
                    }
                }
                
                input.addEventListener('change', toggleFechaFin);
                toggleFechaFin(); // Ejecutar al cargar
            }
        });
    }

    // ========================================
    // File Inputs - Preview y Validación
    // ========================================
    function handleFileInputs() {
        const fileInputs = document.querySelectorAll('input[type="file"]');
        
        fileInputs.forEach(input => {
            input.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (!file) return;

                // Validar tamaño
                const maxSize = 5 * 1024 * 1024; // 5MB
                if (file.size > maxSize) {
                    alert('El archivo es muy grande. Tamaño máximo: 5MB');
                    input.value = '';
                    return;
                }

                // Preview para imágenes
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = function(event) {
                        showImagePreview(input, event.target.result);
                    };
                    reader.readAsDataURL(file);
                }

                // Mostrar nombre del archivo
                showFileName(input, file.name);
            });
        });
    }

    function showImagePreview(input, src) {
        let preview = input.parentElement.querySelector('.image-preview');
        if (!preview) {
            preview = document.createElement('div');
            preview.className = 'image-preview mt-2';
            input.parentElement.appendChild(preview);
        }
        preview.innerHTML = `
            <img src="${src}" alt="Preview" class="img-thumbnail" style="max-width: 200px; max-height: 200px;">
            <button type="button" class="btn btn-sm btn-danger mt-1" onclick="this.parentElement.remove();">
                <i class="bi bi-x"></i> Quitar
            </button>
        `;
    }

    function showFileName(input, fileName) {
        let fileInfo = input.parentElement.querySelector('.file-info');
        if (!fileInfo) {
            fileInfo = document.createElement('small');
            fileInfo.className = 'file-info text-muted d-block mt-1';
            input.parentElement.appendChild(fileInfo);
        }
        fileInfo.textContent = `Archivo: ${fileName}`;
    }

    // ========================================
    // Range Inputs - Mostrar valor actual
    // ========================================
    function handleRangeInputs() {
        const rangeInputs = document.querySelectorAll('input[type="range"]');
        
        rangeInputs.forEach(input => {
            let output = input.nextElementSibling;
            
            if (!output || !output.matches('output')) {
                output = document.createElement('output');
                output.className = 'form-text';
                input.parentElement.appendChild(output);
            }
            
            function updateOutput() {
                const value = input.value;
                output.textContent = `${value}%`;
                
                // Actualizar badge si existe
                const badge = input.parentElement.querySelector('.badge');
                if (badge) {
                    badge.textContent = `${value}%`;
                }
                
                // Color del output basado en el valor
                if (value >= 80) {
                    output.style.color = '#28a745';
                } else if (value >= 50) {
                    output.style.color = '#ffc107';
                } else {
                    output.style.color = '#dc3545';
                }
            }
            
            input.addEventListener('input', updateOutput);
            updateOutput(); // Ejecutar al cargar
        });
    }

    // ========================================
    // Phone Inputs - Formateo automático
    // ========================================
    function handlePhoneInputs() {
        const phoneInputs = document.querySelectorAll('input[type="tel"]');
        
        phoneInputs.forEach(input => {
            input.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                
                // Formatear según la longitud
                if (value.length >= 10) {
                    value = value.substring(0, 10);
                    e.target.value = `(${value.substring(0, 2)}) ${value.substring(2, 6)}-${value.substring(6)}`;
                }
            });
        });
    }

    // ========================================
    // URL Inputs - Validación y formateo
    // ========================================
    function handleURLInputs() {
        const urlInputs = document.querySelectorAll('input[type="url"]');
        
        urlInputs.forEach(input => {
            input.addEventListener('blur', function(e) {
                let value = e.target.value.trim();
                
                if (value && !value.startsWith('http://') && !value.startsWith('https://')) {
                    e.target.value = 'https://' + value;
                }
            });

            input.addEventListener('input', function(e) {
                const value = e.target.value;
                const isValid = isValidURL(value);
                
                if (value && !isValid) {
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });
        });
    }

    function isValidURL(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    // ========================================
    // Character Count - Contador de caracteres
    // ========================================
    function handleCharacterCount() {
        const textareas = document.querySelectorAll('textarea[maxlength]');
        
        textareas.forEach(textarea => {
            const maxLength = textarea.getAttribute('maxlength');
            
            const counter = document.createElement('small');
            counter.className = 'form-text text-muted character-count';
            textarea.parentElement.appendChild(counter);
            
            function updateCounter() {
                const remaining = maxLength - textarea.value.length;
                counter.textContent = `${remaining} caracteres restantes`;
                
                if (remaining < 50) {
                    counter.classList.add('text-warning');
                } else {
                    counter.classList.remove('text-warning');
                }
                
                if (remaining < 0) {
                    counter.classList.add('text-danger');
                } else {
                    counter.classList.remove('text-danger');
                }
            }
            
            textarea.addEventListener('input', updateCounter);
            updateCounter(); // Ejecutar al cargar
        });
    }

    // ========================================
    // Date Validation - Validar fechas
    // ========================================
    function handleDateValidation() {
        const form = document.querySelector('form');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            const fechaInicio = document.querySelector('input[name="fecha_inicio"]');
            const fechaFin = document.querySelector('input[name="fecha_fin"]');
            
            if (fechaInicio && fechaFin && fechaFin.value) {
                const inicio = new Date(fechaInicio.value);
                const fin = new Date(fechaFin.value);
                
                if (fin < inicio) {
                    e.preventDefault();
                    alert('La fecha de finalización no puede ser anterior a la fecha de inicio');
                    fechaFin.focus();
                    return false;
                }
            }
        });
    }

    // ========================================
    // Auto-save (opcional)
    // ========================================
    window.enableAutoSave = function(formId, intervalMs = 60000) {
        const form = document.getElementById(formId);
        if (!form) return;

        setInterval(() => {
            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });
            
            localStorage.setItem(`form_autosave_${formId}`, JSON.stringify(data));
            console.log('Formulario guardado automáticamente');
        }, intervalMs);
    };

    window.restoreAutoSave = function(formId) {
        const saved = localStorage.getItem(`form_autosave_${formId}`);
        if (!saved) return false;

        const form = document.getElementById(formId);
        if (!form) return false;

        const data = JSON.parse(saved);
        
        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = data[key];
            }
        });

        return true;
    };

    // ========================================
    // Form Wizard (multi-step forms)
    // ========================================
    window.FormWizard = function(formId) {
        const form = document.getElementById(formId);
        if (!form) return null;

        const steps = form.querySelectorAll('.form-step');
        let currentStep = 0;

        function showStep(n) {
            steps.forEach((step, index) => {
                step.style.display = index === n ? 'block' : 'none';
            });
            
            currentStep = n;
            updateButtons();
        }

        function updateButtons() {
            const prevBtn = form.querySelector('.btn-prev');
            const nextBtn = form.querySelector('.btn-next');
            const submitBtn = form.querySelector('.btn-submit');

            if (prevBtn) {
                prevBtn.style.display = currentStep === 0 ? 'none' : 'inline-block';
            }

            if (nextBtn) {
                nextBtn.style.display = currentStep === steps.length - 1 ? 'none' : 'inline-block';
            }

            if (submitBtn) {
                submitBtn.style.display = currentStep === steps.length - 1 ? 'inline-block' : 'none';
            }
        }

        return {
            next: () => {
                if (currentStep < steps.length - 1) {
                    showStep(currentStep + 1);
                }
            },
            prev: () => {
                if (currentStep > 0) {
                    showStep(currentStep - 1);
                }
            },
            goTo: (step) => {
                if (step >= 0 && step < steps.length) {
                    showStep(step);
                }
            },
            init: () => {
                showStep(0);
            }
        };
    };

})();
