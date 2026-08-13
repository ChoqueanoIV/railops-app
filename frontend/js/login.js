const API_URL = "http://127.0.0.1:8000";

const loginForm = document.getElementById("login-form");
const matriculaInput = document.getElementById("matricula");
const pinInput = document.getElementById("pin");
const codigoAtivacaoInput = document.getElementById("codigo-ativacao");
const confirmacaoPinInput = document.getElementById("confirmacao-pin");
const campoCodigoAtivacao = document.getElementById("campo-codigo-ativacao");
const campoConfirmacaoPin = document.getElementById("campo-confirmacao-pin");
const pinLabel = document.getElementById("pin-label");
const submitButton = document.getElementById("submit-button");
const alternarModoPergunta = document.getElementById("alternar-modo-pergunta");
const alternarModoButton = document.getElementById("primeiro-acesso");
const mensagem = document.getElementById("mensagem");
let primeiroAcessoAtivo = false;

function exibirMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = tipo;
}

function configurarModoPrimeiroAcesso(ativo) {
    primeiroAcessoAtivo = ativo;
    campoCodigoAtivacao.classList.toggle("oculto", !ativo);
    campoConfirmacaoPin.classList.toggle("oculto", !ativo);
    codigoAtivacaoInput.required = ativo;
    confirmacaoPinInput.required = ativo;
    pinInput.autocomplete = ativo ? "new-password" : "current-password";
    pinLabel.textContent = ativo ? "Novo PIN" : "PIN";
    submitButton.textContent = ativo ? "Definir meu PIN" : "Entrar";
    alternarModoPergunta.textContent = ativo ? "Já defini meu PIN?" : "Primeiro acesso?";
    alternarModoButton.textContent = ativo ? "Voltar para o login" : "Definir meu PIN";
    pinInput.value = "";
    codigoAtivacaoInput.value = "";
    confirmacaoPinInput.value = "";
    exibirMensagem("", "");
}

alternarModoButton.addEventListener("click", function () {
    configurarModoPrimeiroAcesso(!primeiroAcessoAtivo);
});

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const matricula = matriculaInput.value.trim();
    const pin = pinInput.value;

    exibirMensagem("", "");

    if (primeiroAcessoAtivo && pin !== confirmacaoPinInput.value) {
        exibirMensagem("O PIN e a confirmação não coincidem.", "erro");
        return;
    }

    const rota = primeiroAcessoAtivo ? "primeiro-acesso" : "login";
    const corpo = primeiroAcessoAtivo
        ? {
            matricula: matricula,
            codigo_ativacao: codigoAtivacaoInput.value,
            pin: pin,
        }
        : {
            matricula: matricula,
            pin: pin,
        };

    submitButton.disabled = true;
    alternarModoButton.disabled = true;
    submitButton.textContent = "Aguarde...";

    try {
        const response = await fetch(`${API_URL}/auth/${rota}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(corpo),
        });

        const data = await response.json();

        if (!response.ok) {
            const mensagemPadrao = primeiroAcessoAtivo
                ? "Não foi possível definir o PIN."
                : "Não foi possível realizar o login.";
            exibirMensagem(data.detail || mensagemPadrao, "erro");
            return;
        }

        if (primeiroAcessoAtivo) {
            configurarModoPrimeiroAcesso(false);
            exibirMensagem("PIN definido com sucesso. Agora você pode entrar.", "sucesso");
            return;
        }

        exibirMensagem("Login realizado com sucesso.", "sucesso");
        sessionStorage.setItem("access_token", data.access_token);
    } catch (error) {
        exibirMensagem("Não foi possível conectar ao servidor.", "erro");
    } finally {
        submitButton.disabled = false;
        alternarModoButton.disabled = false;
        submitButton.textContent = primeiroAcessoAtivo
            ? "Definir meu PIN"
            : "Entrar";
    }
});
