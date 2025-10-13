document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('contact-form');
    if (!form) return;

    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const messageInput = document.getElementById('message');
    const submitButton = document.getElementById('submit-button');
    const feedbackDiv = document.getElementById('validation-feedback');

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    let currentErrors = [];

    function validateField(input, isEmail = false) {
        const value = input.value.trim();
        let error = '';

        const fieldName = input.id === 'name' ? 'Nombre' :
            input.id === 'email' ? 'Correo electrónico' :
                'Mensaje';

        if (value === '') {
            error = `El campo ${fieldName} es obligatorio.`;
        }

        else if (isEmail && !emailRegex.test(value)) {
            error = "El formato del Correo electrónico es inválido.";
        }

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
        currentErrors = [];

        const nameError = validateField(nameInput);
        if (nameError) currentErrors.push(nameError);

        const emailError = validateField(emailInput, true);
        if (emailError) currentErrors.push(emailError);

        const messageError = validateField(messageInput);
        if (messageError) currentErrors.push(messageError);

        const isValid = currentErrors.length === 0;
        if (currentErrors.length > 0) {
            feedbackDiv.innerHTML = '<ul class="list-unstyled mb-0">' + currentErrors.map(e => `<li><i class="bi bi-x-circle-fill me-2"></i>${e}</li>`).join('') + '</ul>';
        } else {
            feedbackDiv.innerHTML = '';
        }

        submitButton.disabled = !isValid;
    }

    [nameInput, emailInput, messageInput].forEach((input) => {
        input.addEventListener('input', () => {
            input.touched = true;
            validateForm();
        });
        input.addEventListener('blur', () => {
            input.touched = true;
            validateForm();
        });
    });

    submitButton.disabled = true;
    // ✅ Nuevo: mostrar mensaje de éxito
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Evita el envío automático

        validateForm();

        if (currentErrors.length === 0) {
            submitButton.disabled = true;

            try {
                const formData = new FormData(form);

                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    feedbackDiv.innerHTML =
                        '<div class="alert alert-success mt-3" role="alert">' +
                        '<i class="bi bi-check-circle-fill me-2"></i>' +
                        '¡El mensaje fue enviado correctamente!' +
                        '</div>';

                    feedbackDiv.style.color = 'green';
                    form.reset();
                    [nameInput, emailInput, messageInput].forEach((input) => {
                        input.classList.remove('is-valid');
                    });

                    setTimeout(() => {
                        feedbackDiv.innerHTML = '';
                    }, 4000);
                } else {
                    throw new Error('Error al enviar el formulario.');
                }
            } catch (error) {
                feedbackDiv.innerHTML =
                    '<div class="alert alert-danger mt-3" role="alert">' +
                    '<i class="bi bi-exclamation-triangle-fill me-2"></i>' +
                    'Hubo un error al enviar el mensaje. Por favor, intenta nuevamente.' +
                    '</div>';
            } finally {
                submitButton.disabled = false;
            }
        }
    });


});
