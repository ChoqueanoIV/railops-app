const listaEquipe = document.getElementById("lista-equipe");
const adicionarMembroButton = document.getElementById("adicionar-membro");
const listaLinhas = document.getElementById("lista-linhas");
const linhasBrisamar = ["16", "18", "20", "22", "24", "26", "28", "30"];
const mobileOpcoes = document.querySelectorAll('input[name="mobile_utilizado"]');
const campoJustificativaMobile = document.getElementById(
    "campo-justificativa-mobile"
);
const mobileJustificativaInput = document.getElementById("mobile-justificativa");
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

function criarCamposLinhas() {
    linhasBrisamar.forEach(function (codigoLinha) {
        const exigePosicao = codigoLinha === "22" || codigoLinha === "24";
        const linha = document.createElement("div");
        linha.className = "item-linha";
        linha.dataset.codigoLinha = codigoLinha;

        const campoPosicao = exigePosicao
            ? `
                <div class="campo-formulario campo-posicao">
                    <label class="somente-leitor" for="linha-${codigoLinha}-posicao">
                        Posição da linha ${codigoLinha}
                    </label>
                    <select id="linha-${codigoLinha}-posicao" name="linha_sup_inf" required>
                        <option value="">SUP ou INF</option>
                        <option value="SUP">SUP</option>
                        <option value="INF">INF</option>
                    </select>
                </div>
            `
            : '<span class="nao-aplicavel">Não se aplica</span>';

        linha.innerHTML = `
            <strong class="codigo-linha">${codigoLinha}</strong>
            <div class="campo-formulario">
                <label class="somente-leitor" for="linha-${codigoLinha}-veiculos">
                    Veículos ou situação da linha ${codigoLinha}
                </label>
                <input type="text" id="linha-${codigoLinha}-veiculos"
                    name="linha_veiculos" placeholder="Ex.: Livre ou P02, P15">
            </div>
            ${campoPosicao}
        `;

        listaLinhas.appendChild(linha);
    });
}

criarCamposLinhas();

function atualizarJustificativaMobile(event) {
    const mobileNaoUtilizado = event.target.value === "false";
    campoJustificativaMobile.classList.toggle("oculto", !mobileNaoUtilizado);
    mobileJustificativaInput.required = mobileNaoUtilizado;

    if (!mobileNaoUtilizado) {
        mobileJustificativaInput.value = "";
    }
}

mobileOpcoes.forEach(function (opcao) {
    opcao.addEventListener("change", atualizarJustificativaMobile);
});
