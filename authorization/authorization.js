document.addEventListener('DOMContentLoaded', () => {
    const loginTab = document.getElementById('login-tab');
    const registerTab = document.getElementById('register-tab');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const errorMessage = document.getElementById('error-message');

    const switchForm = (showLogin) => {
        if (showLogin) {
            loginTab.classList.add('active');
            registerTab.classList.remove('active');
            loginForm.classList.add('active');
            loginForm.classList.remove('hidden-left');
            registerForm.classList.add('hidden-right');
            registerForm.classList.remove('active');
        } else {
            registerTab.classList.add('active');
            loginTab.classList.remove('active');
            registerForm.classList.add('active');
            registerForm.classList.remove('hidden-right');
            loginForm.classList.add('hidden-left');
            loginForm.classList.remove('active');
        }
    };

    loginTab.addEventListener('click', () => {
        switchForm(true);
    });

    registerTab.addEventListener('click', () => {
        switchForm(false);
    });

    document.getElementById('login-form').addEventListener('submit', (event) => {
        event.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        if (email === '' || password === '') {
            errorMessage.textContent = 'Both fields are required.';
            errorMessage.style.display = 'block';
        } else {
            errorMessage.textContent = '';
            alert('Login successful!');
            // window.location.href = 'calendar.html';
        }
    });

    document.getElementById('register-form').addEventListener('submit', (event) => {
        event.preventDefault();
        const name = document.getElementById('reg-name').value;
        const email = document.getElementById('reg-email').value;
        const password = document.getElementById('reg-password').value;

        if (name === '' || email === '' || password === '') {
            errorMessage.textContent = 'All fields are required.';
            errorMessage.style.display = 'block';
        } else {
            errorMessage.textContent = '';
            alert('Registration successful!');
            // window.location.href = 'calendar.html';
        }
    });

    // Initially show the login form
    switchForm(true);
});
