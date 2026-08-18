const API_URL = "http://127.0.0.1:8000";
const passagemSalva = sessionStorage.getItem("ultima_passagem");

if (!passagemSalva) {
    window.location.replace("./terminal.html");
} else {
    const passagem = JSON.parse(passagemSalva);
    const data = new Date(`${passagem.data}T00:00:00`);
    const passagemEditada = passagem.operacao === "edicao";

    if (passagemEditada) {
        document.getElementById("titulo-confirmacao").textContent =
            "Passagem atualizada com sucesso";
        document.querySelector(".cartao-confirmacao .instrucao").textContent =
            "As alterações foram registradas e a versão anterior foi preservada.";
    }

    document.getElementById("confirmacao-terminal").textContent = passagem.terminal;
    document.getElementById("confirmacao-data").textContent = data.toLocaleDateString(
        "pt-BR"
    );
    document.getElementById("confirmacao-turma").textContent = passagem.turma;
    document.getElementById("confirmacao-turno").textContent =
        passagem.turno === "DIURNO" ? "Diurno — 07h às 19h" : "Noturno — 19h às 07h";
    document.getElementById("confirmacao-protocolo").textContent = passagem.id;
    const outroTerminalLink = document.getElementById("preencher-outro-terminal");
    const passagemEhTecon = passagem.terminal === "Terminal TECON";
    outroTerminalLink.href = passagemEhTecon ? "./brisamar.html" : "./tecon.html";
    outroTerminalLink.textContent = passagemEhTecon
        ? "Preencher passagem do Brisamar agora"
        : "Preencher passagem do TECON agora";

    const editarPassagemLink = document.getElementById("editar-passagem");
    const paginaEdicao = passagemEhTecon ? "tecon.html" : "brisamar.html";
    fetch(`${API_URL}/passagens/${passagem.id}`, {
        headers: { Authorization: `Bearer ${token}` },
    })
        .then(function (response) {
            if (!response.ok) return null;
            return response.json();
        })
        .then(function (dados) {
            if (dados && dados.editavel) {
                editarPassagemLink.href = `./${paginaEdicao}?editar=${passagem.id}`;
                editarPassagemLink.hidden = false;
            }
        })
        .catch(function () {
            editarPassagemLink.hidden = true;
        });
    sessionStorage.removeItem("ultima_passagem");
}
