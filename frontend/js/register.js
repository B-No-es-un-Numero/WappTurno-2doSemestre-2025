document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirmPassword");
  const alertContainer = document.getElementById("alertContainer");

  form.addEventListener("submit", (e) => {
    e.preventDefault(); 

    
    alertContainer.innerHTML = "";

    if (password.value !== confirmPassword.value) {
      showAlert("Las contraseñas no coinciden.", "danger");
      return; 
    }

    
    showAlert("Registro exitoso. Redirigiendo al login...", "success");

    
    setTimeout(() => {
      window.location.href = "login.html";
    }, 2000);
  });

  function showAlert(message, type) {
    const alertHTML = `
      <div class="alert alert-${type} alert-dismissible fade show mt-3" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`;
    alertContainer.innerHTML = alertHTML;
  }
});
