// Navbar toggle
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("nav-links");
hamburger.addEventListener("click", () => {
  navLinks.classList.toggle("show");
});

document.addEventListener("DOMContentLoaded", () => {
  const isLoggedIn = localStorage.getItem("isLoggedIn");
  const authButton = document.getElementById("authButton");
  const profileButton = document.getElementById("profileButton");

  if (isLoggedIn === "true") {
    authButton.style.display = "none";
    profileButton.style.display = "block";
  }
});

// index.js
document.addEventListener("DOMContentLoaded", () => {
    const profileBtn = document.getElementById("profileBtn");

    if (localStorage.getItem("loggedIn") === "true") {
        profileBtn.href = "profile.html"; // Logged in → go to profile
    } else {
        profileBtn.href = "login.html"; // Not logged in → go to login
    }
});


