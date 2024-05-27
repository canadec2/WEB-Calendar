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

    document.getElementById('login-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвратить обычную отправку формы
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
    
        fetch('api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email, password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/calendar.html';
            } else {
                document.getElementById('error-message').textContent = data.message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    
    document.getElementById('register-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const name = document.getElementById('reg-name').value;
        const email = document.getElementById('reg-email').value;
        const password = document.getElementById('reg-password').value;
    
        fetch('api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: name, email: email, password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/calendar.html';
            } else {
                document.getElementById('error-message').textContent = data.message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    

    // Initially show the login form
    switchForm(true);
});
