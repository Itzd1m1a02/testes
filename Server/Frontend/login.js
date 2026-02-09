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
            body: JSON.stringify(loginData) // Transforma em JSON
        });
        if (response.ok) {
            const data = await response.json();
            console.log('Login bem-sucedido:', data);
            // Redirecionar ou mostrar mensagem de sucesso
        }
            else {
            console.error('Erro de login:', response.statusText);
            // Mostrar mensagem de erro para o usuário
        }
    } catch (error) {
        console.error('Erro de conexão:', error);
    }
});