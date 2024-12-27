async function login() {
    console.log("Login function called");
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert('Имя пользователя и пароль обязательны.');
        return;
    }

    const response = await fetch('/auth/login', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'username': username,
            'password': password
        })
    });

    if (response.ok) {
        // Сохраняем имя пользователя в localStorage
        const data = await response.json();
        localStorage.setItem('username', data.username);

        // Перенаправляем на главную страницу после успешного входа
        window.location.href = '/';
    } else {
        const errorData = await response.json();
        alert('Ошибка: ' + errorData.detail);
    }
}
