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

    // Function to handle the POST request
    const sendPostRequest = (url, data) => {
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errData => {
                    throw new Error(errData.message);
                });
            }
            return response.json();
        });
    };

    // Function to handle successful login
    const onSuccessfulLogin = (data) => {
        console.log('Login Success:', data);
        window.location.href = '/calendar.html';
    };

    document.getElementById('login-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        sendPostRequest('/api/login', { login_or_email: email, password: password })
            .then(data => {
                onSuccessfulLogin(data);
            })
            .catch(error => {
                if (error.message.includes('не зарегистрирован')) {
                    errorMessage.textContent = 'Этот логин не зарегистрирован. Пожалуйста, проверьте данные или зарегистрируйтесь.';
                } else {
                    errorMessage.textContent = 'Ошибка входа: ' + error.message;
                }
                document.getElementById('login-password').value = ''; // Сброс поля пароля
            });
    });

    document.getElementById('register-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const name = document.getElementById('reg-name').value;
        const email = document.getElementById('reg-email').value;
        const password = document.getElementById('reg-password').value;

        sendPostRequest('/api/register', { username: name, email: email, password: password })
            .then(data => {
                onSuccessfulLogin(data);
            })
            .catch(error => {
                errorMessage.textContent = 'Ошибка регистрации: ' + error.message;
            });
    });

    switchForm(true);
});
