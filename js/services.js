document.addEventListener("DOMContentLoaded", () => {
  const reserveBtns = document.querySelectorAll(".reserveBtn");

  // reserveBtns.forEach((btn) => {
  //   btn.addEventListener("click", (e) => {
  //     e.preventDefault();

  //     const isLoggedIn = localStorage.getItem("login") === "true";
  //     window.location.href = isLoggedIn ? "new-appointment.html" : "login.html";
  //   });
  // });


  reserveBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();

      const card = btn.closest(".card-body");
      const specialtyName = card.querySelector(".card-title").textContent.trim();

      const isLoggedIn = localStorage.getItem("login") === "true";

      if (isLoggedIn) {
        window.location.href = `new-appointment.html?specialty=${encodeURIComponent(specialtyName)}`;
      } else {
        window.location.href = "login.html";
      }
    });
  });
});
