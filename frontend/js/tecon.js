const listaEquipe = document.getElementById("lista-equipe");
const adicionarMembroButton = document.getElementById("adicionar-membro");
const listaLinhas = document.getElementById("lista-linhas");
const mobileOpcoes = document.querySelectorAll('input[name="mobile_utilizado"]');
const campoJustificativaMobile = document.getElementById(
    "campo-justificativa-mobile"
);
const mobileJustificativaInput = document.getElementById("mobile-justificativa");
const atendimentoOpcoes = document.querySelectorAll(
    'input[name="houve_atendimento"]'
);
const mensagemSemAtendimento = document.getElementById(
    "mensagem-sem-atendimento"
);
const detalhesAtendimento = document.getElementById("detalhes-atendimento");
const cargaOpcoes = document.querySelectorAll(
    'input[name="carga_mal_posicionada"]'
);
const campoDescricaoCarga = document.getElementById("campo-descricao-carga");
const cargaDescricaoInput = document.getElementById("carga-descricao");
const area1AtendidaInput = document.getElementById("area1-atendida");
const area2AtendidaInput = document.getElementById("area2-atendida");
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

function atualizarJustificativaMobile(event) {
    const mobileNaoUtilizado = event.target.value === "false";
    campoJustificativaMobile.classList.toggle("oculto", !mobileNaoUtilizado);
    mobileJustificativaInput.required = mobileNaoUtilizado;

    if (!mobileNaoUtilizado) {
        mobileJustificativaInput.value = "";
    }
}

function atualizarMensagemAtendimento(event) {
    const houveAtendimento = event.target.value === "true";
    mensagemSemAtendimento.classList.toggle("oculto", houveAtendimento);
    detalhesAtendimento.classList.toggle("oculto", !houveAtendimento);

    cargaOpcoes.forEach(function (opcao) {
        opcao.required = houveAtendimento;
    });

    if (!houveAtendimento) {
        limparDetalhesAtendimento();
    }
}

function limparDetalhesAtendimento() {
    cargaOpcoes.forEach(function (opcao) {
        opcao.checked = false;
    });
    cargaDescricaoInput.value = "";
    cargaDescricaoInput.required = false;
    campoDescricaoCarga.classList.add("oculto");

    area1AtendidaInput.checked = false;
    area2AtendidaInput.checked = false;
    atualizarHorariosArea(1, false);
    atualizarHorariosArea(2, false);
}

function atualizarDescricaoCarga(event) {
    const haviaCargaMalPosicionada = event.target.value === "true";
    campoDescricaoCarga.classList.toggle("oculto", !haviaCargaMalPosicionada);
    cargaDescricaoInput.required = haviaCargaMalPosicionada;

    if (!haviaCargaMalPosicionada) {
        cargaDescricaoInput.value = "";
    }
}

function atualizarHorariosArea(numeroArea, atendida) {
    const horarios = document.getElementById(`horarios-area${numeroArea}`);
    const inicio = document.getElementById(`area${numeroArea}-inicio`);
    const termino = document.getElementById(`area${numeroArea}-termino`);
    horarios.classList.toggle("oculto", !atendida);
    inicio.required = atendida;
    termino.required = atendida;

    if (!atendida) {
        inicio.value = "";
        termino.value = "";
    }
}

mobileOpcoes.forEach(function (opcao) {
    opcao.addEventListener("change", atualizarJustificativaMobile);
});

atendimentoOpcoes.forEach(function (opcao) {
    opcao.addEventListener("change", atualizarMensagemAtendimento);
});

cargaOpcoes.forEach(function (opcao) {
    opcao.addEventListener("change", atualizarDescricaoCarga);
});

area1AtendidaInput.addEventListener("change", function () {
    atualizarHorariosArea(1, area1AtendidaInput.checked);
});

area2AtendidaInput.addEventListener("change", function () {
    atualizarHorariosArea(2, area2AtendidaInput.checked);
});
