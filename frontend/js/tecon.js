const listaEquipe = document.getElementById("lista-equipe");
const adicionarMembroButton = document.getElementById("adicionar-membro");
const listaLinhas = document.getElementById("lista-linhas");
const linhasTecon = [
    "Viaduto/DM1A",
    "L1",
    "L2",
    "Travessão",
    "DM4",
    "DM6",
    "DM1",
    "DM3",
    "Funil/DM2",
];
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

function criarCamposLinhas() {
    linhasTecon.forEach(function (codigoLinha, indice) {
        const linha = document.createElement("div");
        linha.className = "item-linha item-linha-tecon";
        linha.dataset.codigoLinha = codigoLinha;
        linha.innerHTML = `
            <strong class="codigo-linha codigo-linha-texto">${codigoLinha}</strong>
            <div class="campo-formulario">
                <label class="somente-leitor" for="linha-${indice}-veiculos">
                    Veículos ou situação da linha ${codigoLinha}
                </label>
                <input type="text" id="linha-${indice}-veiculos"
                    name="linha_veiculos" placeholder="Ex.: Livre ou P02, P15">
            </div>
        `;
        listaLinhas.appendChild(linha);
    });
}

adicionarMembroButton.addEventListener("click", criarCampoMembro);
criarCampoMembro();
criarCamposLinhas();
