document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const submitButton = form.querySelector('button[type="submit"]');

    const validEmail = "turno@admin.com";
    const validPassword = "T12345";

     [emailInput, passwordInput].forEach((input) => {
        input.addEventListener("input", () => {
        if (input.checkValidity()) {
            input.classList.remove("is-invalid");
            input.classList.add("is-valid");
        } else {
            input.classList.remove("is-valid");
            input.classList.add("is-invalid");
        }
        });
    });

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        removeLoginError();

        if (!form.checkValidity()) {
            event.stopPropagation();
            form.classList.add("was-validated");
            return;
        }

        disableSubmit(true);

        setTimeout(() => {
            disableSubmit(false);
            const emailValue = emailInput.value.trim();
            const passwordValue = passwordInput.value.trim();

            if (emailValue === validEmail && passwordValue === validPassword) {
                window.location.href = "./my-appointments.html";
                localStorage.setItem("login", true);
            } else {
                showLoginError("Email o contraseña incorrectos. Intenta nuevamente.");
            }
        }, 2000);
    });

    function showLoginError(message) {
        const errorAlert = document.createElement("div");
        errorAlert.id = "loginError";
        errorAlert.className = "alert alert-danger mt-3";
        errorAlert.textContent = message;
        form.appendChild(errorAlert);
    }

    function removeLoginError() {
        const existingError = document.getElementById("loginError");
        if (existingError) existingError.remove();
    }

    function disableSubmit(state) {
        submitButton.disabled = state;
        if (state) {
            submitButton.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Verificando...
            `;
            submitButton.classList.add("disabled", "opacity-75");
        } else {
            submitButton.innerHTML = "Ingresar";
            submitButton.classList.remove("disabled", "opacity-75");
        }
    }
});
