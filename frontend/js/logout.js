document.addEventListener("DOMContentLoaded", () => {
  const logoutBtn = document.getElementById("logoutBtn");
  if (!logoutBtn) return;

  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("login");
    localStorage.removeItem("appointments");
    
    const currentPath = window.location.pathname;

    if (currentPath.endsWith("index.html") || currentPath === "/") {
      window.location.href = "index.html";
    } else {
      window.location.href = "../index.html";
  }});
});

