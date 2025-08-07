// JavaScript for switching between login and register forms
document.addEventListener('DOMContentLoaded', function() {
    const loginTab = document.getElementById('login-tab');
    const registerTab = document.getElementById('register-tab');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const switchToRegister = document.getElementById('switch-to-register');
    const switchToLogin = document.getElementById('switch-to-login');

    // Switch to Register Form
    function showRegister() {
        loginTab.classList.remove('active');
        registerTab.classList.add('active');
        loginForm.classList.remove('active');
        registerForm.classList.add('active');
    }

    // Switch to Login Form
    function showLogin() {
        registerTab.classList.remove('active');
        loginTab.classList.add('active');
        registerForm.classList.remove('active');
        loginForm.classList.add('active');
    }

    // Tab Click Events
    loginTab.addEventListener('click', showLogin);
    registerTab.addEventListener('click', showRegister);

    // Switch Link Events
    switchToRegister.addEventListener('click', function(e) {
        e.preventDefault();
        showRegister();
    });

    switchToLogin.addEventListener('click', function(e) {
        e.preventDefault();
        showLogin();
    });
});
