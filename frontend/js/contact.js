document.addEventListener("DOMContentLoaded", () => {
    // 1. Obtener elementos del DOM
    const form = document.getElementById('contact-form');
    // Si el formulario existe en la página, iniciamos la lógica.
    if (!form) return; 
    
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const messageInput = document.getElementById('message');
    const submitButton = document.getElementById('submit-button');
    const feedbackDiv = document.getElementById('validation-feedback');

    // Expresión Regular para validar el formato del email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    // Lista para acumular los errores
    let currentErrors = [];

    function validateField(input, isEmail = false) {
        const value = input.value.trim();
        let error = '';
        
        // Asignamos un nombre amigable al campo para el mensaje de error (¡Corrección clave!)
        const fieldName = input.id === 'name' ? 'Nombre' : 
                          input.id === 'email' ? 'Correo electrónico' : 
                          'Mensaje'; 

        // 1. Validar campo obligatorio (No vacío)
        if (value === '') {
            error = `El campo ${fieldName} es obligatorio.`;
        } 
        
        // 2. Si es el campo email, validar el formato
        else if (isEmail && !emailRegex.test(value)) {
            error = "El formato del Correo electrónico es inválido.";
        }
        
        // Aplicar estilos de Bootstrap (rojo si es inválido, verde si es válido)
        if (error) {
            input.classList.add('is-invalid');
            input.classList.remove('is-valid');
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid'); 
        }

        return error;
    }

    function validateForm() {
        currentErrors = []; // Limpiar errores en cada re-evaluación

        // Validar cada campo
        const nameError = validateField(nameInput);
        if (nameError) currentErrors.push(nameError);

        const emailError = validateField(emailInput, true); 
        if (emailError) currentErrors.push(emailError);

        const messageError = validateField(messageInput);
        if (messageError) currentErrors.push(messageError);
        
        const isValid = currentErrors.length === 0;

        // Mostrar Feedback de Errores (usando lista de Bootstrap)
        if (currentErrors.length > 0) {
            // Unir errores en una lista HTML para mejor visualización
            feedbackDiv.innerHTML = '<ul class="list-unstyled mb-0">' + currentErrors.map(e => `<li><i class="bi bi-x-circle-fill me-2"></i>${e}</li>`).join('') + '</ul>';
        } else {
            feedbackDiv.innerHTML = ''; // Limpiar errores
        }

        // Criterio de Aceptación: Deshabilitar/Habilitar el botón.
        submitButton.disabled = !isValid;
    }

    // Escuchar eventos de entrada en todos los campos para validar dinámicamente
    nameInput.addEventListener('input', validateForm);
    emailInput.addEventListener('input', validateForm);
    messageInput.addEventListener('input', validateForm);
    
    // Ejecutar la validación una vez al cargar la página (¡Clave para el estado inicial!)
    validateForm();
});
