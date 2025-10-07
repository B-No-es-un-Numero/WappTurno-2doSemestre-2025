

const navPublic = document.getElementById("navPublic");
const navPrivate = document.getElementById("navPrivate");

const isLoggedIn = localStorage.getItem("login") === "true";

if (isLoggedIn) {
    navPublic.style.display = "none";
    navPrivate.style.display = "block";
} else {
    navPrivate.style.display = "none";
    navPublic.style.display = "block";
}



