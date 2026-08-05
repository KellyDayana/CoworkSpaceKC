/**
 * Sistema de Validaciones para CoworkSpace KC
 * Valida campos de formularios en tiempo real
 */

// Validar Cédula Ecuatoriana (10 dígitos)
function validarCedulaEcuatoriana(cedula) {
    cedula = cedula.trim();
    
    // Debe tener 10 dígitos
    if (cedula.length !== 10) {
        return {
            valido: false,
            mensaje: 'La cédula debe tener exactamente 10 dígitos'
        };
    }
    
    // Solo números
    if (!/^\d{10}$/.test(cedula)) {
        return {
            valido: false,
            mensaje: 'La cédula solo debe contener números'
        };
    }
    
    // Validar provincia (primeros 2 dígitos)
    const provincia = parseInt(cedula.substr(0, 2));
    if (provincia < 1 || provincia > 24) {
        return {
            valido: false,
            mensaje: 'Los primeros 2 dígitos deben ser entre 01 y 24 (código de provincia)'
        };
    }
    
    // Validar dígito verificador (algoritmo módulo 10)
    const digitoVerificador = parseInt(cedula.charAt(9));
    let suma = 0;
    
    for (let i = 0; i < 9; i++) {
        let digito = parseInt(cedula.charAt(i));
        
        if (i % 2 === 0) {  // Posiciones impares (0, 2, 4, 6, 8)
            digito *= 2;
            if (digito > 9) {
                digito -= 9;
            }
        }
        suma += digito;
    }
    
    const resultado = suma % 10;
    const digitoEsperado = resultado === 0 ? 0 : 10 - resultado;
    
    if (digitoVerificador !== digitoEsperado) {
        return {
            valido: false,
            mensaje: 'Cédula inválida. El dígito verificador no coincide'
        };
    }
    
    return {
        valido: true,
        mensaje: 'Cédula válida'
    };
}

// Validar RUC Ecuatoriano (13 dígitos)
function validarRUC(ruc) {
    ruc = ruc.trim();
    
    if (ruc.length !== 13) {
        return {
            valido: false,
            mensaje: 'El RUC debe tener exactamente 13 dígitos'
        };
    }
    
    if (!/^\d{13}$/.test(ruc)) {
        return {
            valido: false,
            mensaje: 'El RUC solo debe contener números'
        };
    }
    
    // Los últimos 3 dígitos deben ser 001 (por lo general)
    const establecimiento = ruc.substr(10, 3);
    if (!/^\d{3}$/.test(establecimiento)) {
        return {
            valido: false,
            mensaje: 'El RUC debe terminar con 3 dígitos (código de establecimiento)'
        };
    }
    
    return {
        valido: true,
        mensaje: 'RUC válido'
    };
}

// Validar Email
function validarEmail(email) {
    const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    
    if (!regex.test(email)) {
        return {
            valido: false,
            mensaje: 'Email inválido. Formato correcto: ejemplo@dominio.com'
        };
    }
    
    return {
        valido: true,
        mensaje: 'Email válido'
    };
}

// Validar Teléfono (Ecuador: 10 dígitos, empieza con 09 o 07 para móviles)
function validarTelefono(telefono) {
    telefono = telefono.trim();
    
    if (telefono.length < 9 || telefono.length > 10) {
        return {
            valido: false,
            mensaje: 'El teléfono debe tener entre 9 y 10 dígitos'
        };
    }
    
    if (!/^\d+$/.test(telefono)) {
        return {
            valido: false,
            mensaje: 'El teléfono solo debe contener números'
        };
    }
    
    return {
        valido: true,
        mensaje: 'Teléfono válido'
        };
}

// Validar Solo Letras (nombres, apellidos)
function validarSoloLetras(texto, campo) {
    const regex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
    
    if (!regex.test(texto)) {
        return {
            valido: false,
            mensaje: `${campo} solo debe contener letras`
        };
    }
    
    if (texto.trim().length < 2) {
        return {
            valido: false,
            mensaje: `${campo} debe tener al menos 2 caracteres`
        };
    }
    
    return {
        valido: true,
        mensaje: `${campo} válido`
    };
}

// Validar Números Positivos
function validarNumeroPositivo(numero, campo) {
    if (isNaN(numero) || numero <= 0) {
        return {
            valido: false,
            mensaje: `${campo} debe ser un número positivo`
        };
    }
    
    return {
        valido: true,
        mensaje: `${campo} válido`
    };
}

// Validar Fecha no en el Pasado
function validarFechaFutura(fecha, campo) {
    const fechaIngresada = new Date(fecha);
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    
    if (fechaIngresada < hoy) {
        return {
            valido: false,
            mensaje: `${campo} no puede ser en el pasado`
        };
    }
    
    return {
        valido: true,
        mensaje: `${campo} válida`
    };
}

// Mostrar Error en Campo
function mostrarError(input, mensaje) {
    // Eliminar error previo
    const errorPrevio = input.parentElement.querySelector('.error-mensaje');
    if (errorPrevio) {
        errorPrevio.remove();
    }
    
    // Agregar clase de error
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
    
    // Crear mensaje de error
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-mensaje invalid-feedback d-block';
    errorDiv.innerHTML = '<i class="fa fa-exclamation-circle"></i> ' + mensaje;
    errorDiv.style.color = '#dc3545';
    errorDiv.style.fontSize = '14px';
    errorDiv.style.marginTop = '5px';
    
    input.parentElement.appendChild(errorDiv);
}

// Mostrar Éxito en Campo
function mostrarExito(input, mensaje) {
    // Eliminar error previo
    const errorPrevio = input.parentElement.querySelector('.error-mensaje');
    if (errorPrevio) {
        errorPrevio.remove();
    }
    
    // Agregar clase de éxito
    input.classList.add('is-valid');
    input.classList.remove('is-invalid');
    
    // Crear mensaje de éxito
    const exitoDiv = document.createElement('div');
    exitoDiv.className = 'error-mensaje valid-feedback d-block';
    exitoDiv.innerHTML = '<i class="fa fa-check-circle"></i> ' + mensaje;
    exitoDiv.style.color = '#28a745';
    exitoDiv.style.fontSize = '14px';
    exitoDiv.style.marginTop = '5px';
    
    input.parentElement.appendChild(exitoDiv);
}

// Limpiar validación
function limpiarValidacion(input) {
    input.classList.remove('is-valid', 'is-invalid');
    const errorPrevio = input.parentElement.querySelector('.error-mensaje');
    if (errorPrevio) {
        errorPrevio.remove();
    }
}

// Inicializar validaciones en formularios
document.addEventListener('DOMContentLoaded', function() {
    // ==================== VISTA PREVIA DE ARCHIVOS ====================
    // Vista previa de PDFs e Imágenes en inputs tipo file
    const inputsFile = document.querySelectorAll('input[type="file"]');
    inputsFile.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            const maxSize = 5 * 1024 * 1024; // 5MB
            if (file.size > maxSize) {
                Swal.fire({
                    icon: 'error',
                    title: 'Archivo muy grande',
                    text: 'El archivo no debe superar 5MB',
                    confirmButtonColor: '#4A6785'
                });
                this.value = '';
                return;
            }
            
            // Crear contenedor de vista previa si no existe
            let previewContainer = this.parentElement.querySelector('.file-preview-container');
            if (!previewContainer) {
                previewContainer = document.createElement('div');
                previewContainer.className = 'file-preview-container mt-3';
                this.parentElement.appendChild(previewContainer);
            }
            
            // Limpiar vista previa anterior
            previewContainer.innerHTML = '';
            
            const fileType = file.type;
            const fileName = file.name;
            const fileSize = (file.size / 1024).toFixed(2) + ' KB';
            
            if (fileType === 'application/pdf') {
                // Vista previa de PDF
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewContainer.innerHTML = `
                        <div class="card border-danger">
                            <div class="card-header bg-danger text-white">
                                <i class="fa fa-file-pdf"></i> Vista Previa PDF
                            </div>
                            <div class="card-body">
                                <embed src="${e.target.result}" type="application/pdf" width="100%" height="400px" />
                                <div class="mt-2">
                                    <strong>Archivo:</strong> ${fileName}<br>
                                    <strong>Tamaño:</strong> ${fileSize}
                                </div>
                            </div>
                        </div>
                    `;
                };
                reader.readAsDataURL(file);
            } else if (fileType.startsWith('image/')) {
                // Vista previa de Imagen
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewContainer.innerHTML = `
                        <div class="card border-primary">
                            <div class="card-header bg-primary text-white">
                                <i class="fa fa-image"></i> Vista Previa Imagen
                            </div>
                            <div class="card-body text-center">
                                <img src="${e.target.result}" class="img-fluid rounded shadow-sm" 
                                     style="max-height: 400px;" alt="Vista previa">
                                <div class="mt-2">
                                    <strong>Archivo:</strong> ${fileName}<br>
                                    <strong>Tamaño:</strong> ${fileSize}
                                </div>
                            </div>
                        </div>
                    `;
                };
                reader.readAsDataURL(file);
            } else {
                // Otros archivos
                previewContainer.innerHTML = `
                    <div class="alert alert-info">
                        <i class="fa fa-file"></i> <strong>${fileName}</strong> (${fileSize})
                    </div>
                `;
            }
        });
    });
    
    // Validar Cédulas
    const inputsCedula = document.querySelectorAll('input[name="cedula"]');
    inputsCedula.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                const resultado = validarCedulaEcuatoriana(this.value);
                if (resultado.valido) {
                    mostrarExito(this, resultado.mensaje);
                } else {
                    mostrarError(this, resultado.mensaje);
                }
            }
        });
        
        input.addEventListener('input', function() {
            // Solo permitir números
            this.value = this.value.replace(/\D/g, '').substring(0, 10);
        });
    });
    
    // Validar RUCs
    const inputsRUC = document.querySelectorAll('input[name="ruc"]');
    inputsRUC.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                const resultado = validarRUC(this.value);
                if (resultado.valido) {
                    mostrarExito(this, resultado.mensaje);
                } else {
                    mostrarError(this, resultado.mensaje);
                }
            }
        });
        
        input.addEventListener('input', function() {
            // Solo permitir números
            this.value = this.value.replace(/\D/g, '').substring(0, 13);
        });
    });
    
    // Validar Emails
    const inputsEmail = document.querySelectorAll('input[type="email"]');
    inputsEmail.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                const resultado = validarEmail(this.value);
                if (resultado.valido) {
                    mostrarExito(this, resultado.mensaje);
                } else {
                    mostrarError(this, resultado.mensaje);
                }
            }
        });
    });
    
    // Validar Teléfonos
    const inputsTelefono = document.querySelectorAll('input[name="telefono"]');
    inputsTelefono.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                const resultado = validarTelefono(this.value);
                if (resultado.valido) {
                    mostrarExito(this, resultado.mensaje);
                } else {
                    mostrarError(this, resultado.mensaje);
                }
            }
        });
        
        input.addEventListener('input', function() {
            // Solo permitir números
            this.value = this.value.replace(/\D/g, '').substring(0, 10);
        });
    });
    
    // Validar Nombres y Apellidos
    const inputsNombre = document.querySelectorAll('input[name="nombre"], input[name="apellido"]');
    inputsNombre.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                const campo = this.name === 'nombre' ? 'Nombre' : 'Apellido';
                const resultado = validarSoloLetras(this.value, campo);
                if (resultado.valido) {
                    mostrarExito(this, resultado.mensaje);
                } else {
                    mostrarError(this, resultado.mensaje);
                }
            }
        });
        
        input.addEventListener('input', function() {
            // Solo permitir letras y espacios
            this.value = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
        });
    });
    
    // Prevenir submit si hay errores
    const formularios = document.querySelectorAll('form');
    formularios.forEach(form => {
        form.addEventListener('submit', function(e) {
            const camposInvalidos = this.querySelectorAll('.is-invalid');
            if (camposInvalidos.length > 0) {
                e.preventDefault();
                Swal.fire({
                    icon: 'error',
                    title: 'Errores en el formulario',
                    text: 'Por favor corrige los errores marcados en rojo antes de continuar.',
                    confirmButtonColor: '#4A6785'
                });
                // Focus en el primer campo inválido
                camposInvalidos[0].focus();
            }
        });
    });
});
