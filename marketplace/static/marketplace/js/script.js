const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

// Toggle forms
registerBtn.addEventListener('click', () => {
    container.classList.add('active');
});
loginBtn.addEventListener('click', () => {
    container.classList.remove('active');
});

// Handle Registration Submit
const registerForm = document.querySelector('#registerForm'); 
if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
        e.preventDefault(); 
        // ✅ Fake success for now
        alert("Registration successful!");
        window.location.href = "profile1.html"; 
    });
}

// Handle Login Submit
const loginForm = document.querySelector('#loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault(); 
        // ✅ Fake success for now
        alert("Login successful!");
        window.location.href = "index.html"; 
    });
}
