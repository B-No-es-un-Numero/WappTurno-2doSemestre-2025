document.addEventListener("DOMContentLoaded", () => {
  const reserveBtns = document.querySelectorAll(".reserveBtn");

  reserveBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();

      const isLoggedIn = localStorage.getItem("login") === "true";
      window.location.href = isLoggedIn ? "new-appointment.html" : "login.html";
    });
  });
});
