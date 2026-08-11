const API_URL = "http://127.0.0.1:8000";

const loginForm = document.getElementById("login-form");
const matriculaInput = document.getElementById("matricula");
const pinInput = document.getElementById("pin");
const mensagem = document.getElementById("mensagem");

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const matricula = matriculaInput.value.trim();
    const pin = pinInput.value;

    mensagem.textContent = "";
    mensagem.className = "";

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                matricula: matricula,
                pin: pin,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            mensagem.textContent = data.detail || "Não foi possível realizar o login.";
            mensagem.className = "erro";
            return;
        }

        mensagem.textContent = "Login realizado com sucesso.";
        mensagem.className = "sucesso";

        sessionStorage.setItem("access_token", data.access_token);
    } catch (error) {
        mensagem.textContent = "Não foi possível conectar ao servidor.";
        mensagem.className = "erro";
    }
});
