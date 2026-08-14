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
    document.getElementById("confirmacao-turno").textContent = passagem.turno;
    document.getElementById("confirmacao-protocolo").textContent = passagem.id;
    sessionStorage.removeItem("ultima_passagem");
}
