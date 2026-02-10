const formulario = document.querySelector('form');

formulario.addEventListener('submit', async (event) => {
    event.preventDefault(); 

  
    const email = document.getElementById('email').value;
    const senha = document.getElementById('password').value;
    const confirmarSenha = document.getElementById('confirm-password').value;
    const cpf = document.getElementById('cpf').value;
    const nascimento = document.getElementById('birthdate').value;

    if (senha !== confirmarSenha) {
        alert("As senhas não coincidem!");
        return;
    }

    const dadosCadastro = {
        email: email,
        senha: senha,
        cpf: cpf,
        nascimento: nascimento
    };

    try {
        const response = await fetch('http://localhost:8000/cadastro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dadosCadastro)
        });

        const resultado = await response.json();

        if (response.ok) {
            alert(resultado.mensagem);
            window.location.href = "/static/Login.html";
        } else {
            alert("Erro no cadastro: " + resultado.mensagem);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert("Erro ao conectar com o servidor.");
    }
});