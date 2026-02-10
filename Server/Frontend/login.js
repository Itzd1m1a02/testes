const formulario = document.querySelector('form');

formulario.addEventListener('submit', async (event) => {
    event.preventDefault(); 

    const email = document.getElementById('email').value;
    const senha = document.getElementById('password').value;
    const loginData = { email, senha };

    try {
        const response = await fetch('http://localhost:8000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(loginData)
        });

        const data = await response.json();

        if (data.status === 200) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('usuario', email);

            alert("Login OK! Redirecionando...");
            window.location.href = "/static/home.html";
        } else {
            alert("Erro: " + data.mensagem);
        }

    } catch (error) {
        console.error('Erro de conexão:', error);
        alert("Erro ao conectar com o servidor");
    }
});