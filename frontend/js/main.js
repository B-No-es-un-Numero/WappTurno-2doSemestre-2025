document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector("header");
    const loginStatus = localStorage.getItem("login");
    const isLoggedIn = loginStatus === "true";

    if (!isLoggedIn) {
      header.innerHTML = `
          <div class="container">
            <h1 class="display-5 fw-bold text-primary">
              <i class="bi bi-hospital"></i> Bienvenido a WappTurno
            </h1>
            <p class="lead text-body">Tu sistema de reservas médicas rápido, seguro y sencillo.</p>
            <div class="mt-4">
              <a href="./pages/login.html" class="btn btn-primary btn-lg me-2">
                <i class="bi bi-box-arrow-in-right"></i> Ingresar
              </a>
              <a href="./pages/register.html" class="btn btn-outline-primary btn-lg">
                <i class="bi bi-person-plus"></i> Registrarse
              </a>
            </div>
          </div>
      `;
    } else {
      header.innerHTML = `
        <div class="container">
            <h1 class="display-5 fw-bold text-primary">
              <i class="bi bi-hospital"></i> Bienvenido a WappTurno
            </h1>
            <p class="lead text-body">Tu sistema de reservas médicas rápido, seguro y sencillo.</p>
            <div class="mt-4">
              <a href="./pages/new-appointment.html" class="btn btn-primary btn-lg me-2">
                <i class="bi bi-box-arrow-in-right"></i> Nuevo turno
              </a>
              <a href="./pages/my-appointments.html" class="btn btn-outline-primary btn-lg">
                <i class="bi bi-person-plus"></i> Mis turnos
              </a>
            </div>
        </div>
      `;

      // Agregamos funcionalidad al botón de cerrar sesión
      document.getElementById("logoutBtn").addEventListener("click", () => {
        localStorage.setItem("login", "false");
        location.reload(); // recarga para que se actualice el header
      });
    }
  });