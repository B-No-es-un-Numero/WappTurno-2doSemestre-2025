document.addEventListener("DOMContentLoaded", () => {
    // 1. Obtener elementos del DOM (usando los IDs que añadimos en el HTML)
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

    function validateField(input, isEmail = false) {
        const value = input.value.trim();
        let error = '';

        // Validar campo obligatorio (No vacío)
        if (value === '') {
            error = `El campo ${input.placeholder.split(' ')[0]} es obligatorio.`;
        } 
        
        // Si es el campo email, validar el formato
        else if (isEmail && !emailRegex.test(value)) {
            error = "El formato del Email es inválido.";
        }
        
        // Mostrar o remover la clase 'is-invalid' de Bootstrap
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
        let errors = [];

        // Validar cada campo
        const nameError = validateField(nameInput);
        if (nameError) errors.push(nameError);

        const emailError = validateField(emailInput, true); // true para validar formato email
        if (emailError) errors.push(emailError);

        const messageError = validateField(messageInput);
        if (messageError) errors.push(messageError);
        
        const isValid = errors.length === 0;

        // Mostrar Feedback de Errores
        if (errors.length > 0) {
            feedbackDiv.innerHTML = '<ul>' + errors.map(e => `<li>${e}</li>`).join('') + '</ul>';
        } else {
            feedbackDiv.innerHTML = ''; // Limpiar errores
        }

        // Criterio de Aceptación: Si todo está correcto, se habilita el botón de envío.
        submitButton.disabled = !isValid;
        
        // Si hay errores, deshabilitar el botón forzosamente (aunque el usuario no haya escrito nada aún)
        if (!isValid) {
            submitButton.classList.add('disabled', 'opacity-75');
        } else {
             submitButton.classList.remove('disabled', 'opacity-75');
        }

        return isValid;
    }

    // Escuchar eventos de entrada en todos los campos para validar dinámicamente
    // Cada vez que el usuario escriba, se re-evalúa el formulario.
    nameInput.addEventListener('input', validateForm);
    emailInput.addEventListener('input', validateForm);
    messageInput.addEventListener('input', validateForm);
    
    // Ejecutar la validación una vez al cargar la página para que el botón esté deshabilitado inicialmente.
    validateForm();
});
