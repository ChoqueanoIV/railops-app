const passagemSalva = sessionStorage.getItem("ultima_passagem");

if (!passagemSalva) {
    window.location.replace("./terminal.html");
} else {
    const passagem = JSON.parse(passagemSalva);
    const data = new Date(`${passagem.data}T00:00:00`);

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
    sessionStorage.removeItem("ultima_passagem");
}
