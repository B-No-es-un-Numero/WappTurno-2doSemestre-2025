document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirmPassword");
  const alertContainer = document.getElementById("alertContainer");
  const message = document.getElementById('passwordMessage');
  const submitBtn = document.getElementById("submitBtn");
  const dniInput = document.getElementById("dni");
  const inputs = form.querySelectorAll("input[required]");

  submitBtn.disabled = true;

  function showAlert(message, type) {
    const alertHTML = `
      <div class="alert alert-${type} alert-dismissible fade show mt-3" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`;
    alertContainer.innerHTML = alertHTML;
  }

  function checkPasswordMatch() {
    if (confirmPassword.value === '') {
      message.classList.add('d-none');
      confirmPassword.classList.remove('is-invalid', 'is-valid');
      submitBtn.disabled = true;
      return;
    }

    if (password.value === confirmPassword.value) {
      message.classList.add('d-none');
      confirmPassword.classList.remove('is-invalid');
      confirmPassword.classList.add('is-valid');
      submitBtn.disabled = false;
    } else {
      message.classList.remove('d-none');
      confirmPassword.classList.remove('is-valid');
      confirmPassword.classList.add('is-invalid');
      submitBtn.disabled = true;
    }
  }

  password.addEventListener('input', checkPasswordMatch);
  confirmPassword.addEventListener('input', checkPasswordMatch);

  dniInput.addEventListener("input", (e) => {
    e.target.value = e.target.value.replace(/\D/g, ""); 
    if (e.target.value.length > 8) {
      e.target.value = e.target.value.slice(0, 8); 
    }
    validateInput(e.target);
  });

  inputs.forEach((input) => {
    input.addEventListener("input", () => validateInput(input));
  });

  function validateInput(input) {
    const min = input.getAttribute("minlength") || 0;
    const max = input.getAttribute("maxlength") || Infinity;
    const valueLength = input.value.trim().length;
    const isValidLength = valueLength >= min && valueLength <= max;

    if (input.type === "email") {
      const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value);
      toggleValidation(input, isValidEmail);
    } else if (input.id === "confirmPassword") {
      toggleValidation(input, input.value === password.value && valueLength >= 6);
    } else {
      toggleValidation(input, isValidLength);
    }
  }

  function toggleValidation(input, isValid) {
    if (isValid) {
      input.classList.add("is-valid");
      input.classList.remove("is-invalid");
    } else {
      input.classList.add("is-invalid");
      input.classList.remove("is-valid");
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    alertContainer.innerHTML = "";


    let allValid = true;
    inputs.forEach((input) => {
      validateInput(input);
      if (!input.classList.contains("is-valid")) {
        allValid = false;
      }
    });

    const dniValue = parseInt(dniInput.value);
    if (dniValue < 1000000 || dniValue > 99999999 || isNaN(dniValue)) {
      showAlert("El DNI debe estar entre 1.000.000 y 99.999.999.", "danger");
      dniInput.classList.add("is-invalid");
      return;
    }

    if (!allValid) {
      showAlert("Por favor, complete correctamente todos los campos.", "danger");
      return;
    }

    showAlert("Registro exitoso. Redirigiendo al login...", "success");
    setTimeout(() => {
      window.location.href = "login.html";
    }, 2000);
  });
});