const listaEquipe = document.getElementById("lista-equipe");
const adicionarMembroButton = document.getElementById("adicionar-membro");
let proximoMembroId = 1;

function atualizarBotoesRemover() {
    const membros = listaEquipe.querySelectorAll(".membro-equipe");

    membros.forEach(function (membro) {
        membro.querySelector(".botao-remover").hidden = membros.length === 1;
    });
}

function criarCampoMembro() {
    const membroId = proximoMembroId;
    proximoMembroId += 1;

    const membro = document.createElement("div");
    membro.className = "item-dinamico membro-equipe";
    membro.dataset.membroId = membroId;
    membro.innerHTML = `
        <div class="campo-formulario">
            <label for="membro-nome-${membroId}">Nome</label>
            <input type="text" id="membro-nome-${membroId}"
                name="equipe_nome" autocomplete="name" required>
        </div>
        <div class="campo-formulario">
            <label for="membro-matricula-${membroId}">Matrícula</label>
            <input type="text" id="membro-matricula-${membroId}"
                name="equipe_matricula" inputmode="numeric" minlength="8"
                maxlength="8" pattern="[0-9]{8}"
                title="A matrícula deve conter exatamente 8 números" required>
        </div>
        <button type="button" class="botao-remover" aria-label="Remover membro">
            Remover
        </button>
    `;

    membro.querySelector(".botao-remover").addEventListener("click", function () {
        membro.remove();
        atualizarBotoesRemover();
    });

    listaEquipe.appendChild(membro);
    atualizarBotoesRemover();
    membro.querySelector("input").focus();
}

adicionarMembroButton.addEventListener("click", criarCampoMembro);
criarCampoMembro();
