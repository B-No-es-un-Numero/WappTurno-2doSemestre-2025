document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const submitButton = form.querySelector('button[type="submit"]');

    const validEmail = "turno@admin.com";
    const validPassword = "T12345";

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        emailInput.classList.remove("is-invalid");
        passwordInput.classList.remove("is-invalid");
        removeLoginError();

        const emailValue = emailInput.value.trim();
        const passwordValue = passwordInput.value.trim();
        let isValid = true;

        if (!emailValue || !emailInput.checkValidity()) {
            emailInput.classList.add("is-invalid");
            isValid = false;
        }

        if (!passwordValue || passwordValue.length !== 6) {
            passwordInput.classList.add("is-invalid");
            isValid = false;
        }

        if (!isValid) return;

        disableSubmit(true);

        setTimeout(() => {
            disableSubmit(false);

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
