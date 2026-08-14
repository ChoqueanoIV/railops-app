const API_URL = "http://127.0.0.1:8000";
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
const listaRadios = document.getElementById("lista-radios");
const radiosVazio = document.getElementById("radios-vazio");
const adicionarRadioButton = document.getElementById("adicionar-radio");
const formularioTecon = document.getElementById("formulario-tecon");
const enviarPassagemButton = document.getElementById("enviar-passagem");
const mensagemEnvio = document.getElementById("mensagem-envio");
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
let proximoRadioId = 1;

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

function atualizarEstadoRadios() {
    radiosVazio.hidden = listaRadios.children.length > 0;
}

function atualizarOrdemRadios() {
    listaRadios.querySelectorAll(".item-radio").forEach(function (radio, indice) {
        radio.querySelector(".ordem-radio").textContent = indice + 1;
    });
}

function criarCampoRadio() {
    const radioId = proximoRadioId;
    proximoRadioId += 1;
    const radio = document.createElement("div");
    radio.className = "item-radio";
    radio.dataset.radioId = radioId;
    radio.innerHTML = `
        <div class="cabecalho-item-radio">
            <strong>Rádio <span class="ordem-radio"></span></strong>
            <button type="button" class="botao-remover">Remover</button>
        </div>
        <div class="grade-formulario grade-radio">
            <div class="campo-formulario">
                <label for="radio-${radioId}-numero">Número</label>
                <input type="text" id="radio-${radioId}-numero"
                    name="radio_numero" required>
            </div>
            <div class="campo-formulario campo-manobrador">
                <label for="radio-${radioId}-manobrador">Manobrador</label>
                <input type="text" id="radio-${radioId}-manobrador"
                    name="radio_manobrador" required>
            </div>
            <div class="campo-formulario">
                <label for="radio-${radioId}-retirada">Retirada</label>
                <input type="time" id="radio-${radioId}-retirada"
                    name="radio_hora_retirada">
            </div>
            <div class="campo-formulario">
                <label for="radio-${radioId}-entrega">Entrega</label>
                <input type="time" id="radio-${radioId}-entrega"
                    name="radio_hora_entrega">
            </div>
        </div>
        <label class="opcao-checkbox">
            <input type="checkbox" name="radio_apresentou_falha">
            <span>O rádio apresentou falha</span>
        </label>
        <div class="campo-formulario campo-falha oculto">
            <label for="radio-${radioId}-falha">Descrição da falha</label>
            <textarea id="radio-${radioId}-falha" name="radio_falha_descricao"
                rows="2"></textarea>
        </div>
    `;

    const falhaCheckbox = radio.querySelector('[name="radio_apresentou_falha"]');
    const campoFalha = radio.querySelector(".campo-falha");
    const falhaDescricao = radio.querySelector('[name="radio_falha_descricao"]');
    falhaCheckbox.addEventListener("change", function () {
        campoFalha.classList.toggle("oculto", !falhaCheckbox.checked);
        falhaDescricao.required = falhaCheckbox.checked;
        if (!falhaCheckbox.checked) {
            falhaDescricao.value = "";
        }
    });
    radio.querySelector(".botao-remover").addEventListener("click", function () {
        radio.remove();
        atualizarOrdemRadios();
        atualizarEstadoRadios();
    });
    listaRadios.appendChild(radio);
    atualizarOrdemRadios();
    atualizarEstadoRadios();
    radio.querySelector("input").focus();
}

function valorOuNulo(valor) {
    const texto = valor.trim();
    return texto === "" ? null : texto;
}

function montarEquipe() {
    return Array.from(listaEquipe.querySelectorAll(".membro-equipe")).map(
        function (membro) {
            return {
                nome: membro.querySelector('[name="equipe_nome"]').value,
                matricula: membro.querySelector('[name="equipe_matricula"]').value,
            };
        }
    );
}

function montarOcupacoesLinhas() {
    return Array.from(listaLinhas.querySelectorAll(".item-linha")).map(
        function (linha) {
            return {
                codigo_linha: linha.dataset.codigoLinha,
                veiculos: valorOuNulo(
                    linha.querySelector('[name="linha_veiculos"]').value
                ),
                sup_inf: null,
            };
        }
    );
}

function montarRadiosUtilizados() {
    return Array.from(listaRadios.querySelectorAll(".item-radio")).map(
        function (radio) {
            const apresentouFalha = radio.querySelector(
                '[name="radio_apresentou_falha"]'
            ).checked;
            return {
                numero: radio.querySelector('[name="radio_numero"]').value,
                manobrador_nome: radio.querySelector(
                    '[name="radio_manobrador"]'
                ).value,
                hora_retirada: valorOuNulo(
                    radio.querySelector('[name="radio_hora_retirada"]').value
                ),
                hora_entrega: valorOuNulo(
                    radio.querySelector('[name="radio_hora_entrega"]').value
                ),
                apresentou_falha: apresentouFalha,
                falha_descricao: apresentouFalha
                    ? valorOuNulo(
                        radio.querySelector('[name="radio_falha_descricao"]').value
                    )
                    : null,
            };
        }
    );
}

function montarDetalheTecon() {
    const houveAtendimento = formularioTecon.querySelector(
        '[name="houve_atendimento"]:checked'
    ).value === "true";
    if (!houveAtendimento) {
        return { houve_atendimento: false };
    }
    const cargaMalPosicionada = formularioTecon.querySelector(
        '[name="carga_mal_posicionada"]:checked'
    ).value === "true";
    return {
        houve_atendimento: true,
        carga_mal_posicionada: cargaMalPosicionada,
        carga_mal_posicionada_descricao: cargaMalPosicionada
            ? valorOuNulo(cargaDescricaoInput.value)
            : null,
        area1_atendida: area1AtendidaInput.checked,
        area1_inicio: area1AtendidaInput.checked
            ? valorOuNulo(document.getElementById("area1-inicio").value)
            : null,
        area1_termino: area1AtendidaInput.checked
            ? valorOuNulo(document.getElementById("area1-termino").value)
            : null,
        area2_atendida: area2AtendidaInput.checked,
        area2_inicio: area2AtendidaInput.checked
            ? valorOuNulo(document.getElementById("area2-inicio").value)
            : null,
        area2_termino: area2AtendidaInput.checked
            ? valorOuNulo(document.getElementById("area2-termino").value)
            : null,
    };
}

function montarPassagem() {
    const mobileUtilizado = formularioTecon.querySelector(
        '[name="mobile_utilizado"]:checked'
    ).value === "true";
    return {
        data: document.getElementById("data").value,
        turno: document.getElementById("turno").value,
        observacoes: document.getElementById("observacoes").value,
        relatorio_ocorrencias: document.getElementById(
            "relatorio-ocorrencias"
        ).value,
        mobile_utilizado: mobileUtilizado,
        mobile_justificativa: mobileUtilizado
            ? null
            : valorOuNulo(mobileJustificativaInput.value),
        equipe: montarEquipe(),
        ocupacoes_linhas: montarOcupacoesLinhas(),
        detalhe: montarDetalheTecon(),
        radios_utilizados: montarRadiosUtilizados(),
    };
}

function exibirMensagemEnvio(texto) {
    mensagemEnvio.textContent = texto;
    mensagemEnvio.className = "erro";
}

function extrairMensagemErro(dados) {
    if (typeof dados.detail === "string") {
        return dados.detail;
    }
    if (Array.isArray(dados.detail) && dados.detail.length > 0) {
        return dados.detail[0].msg || "Verifique os campos informados.";
    }
    return "Não foi possível registrar a passagem de serviço.";
}

adicionarRadioButton.addEventListener("click", criarCampoRadio);
atualizarEstadoRadios();

formularioTecon.addEventListener("submit", async function (event) {
    event.preventDefault();
    mensagemEnvio.textContent = "";
    mensagemEnvio.className = "";
    enviarPassagemButton.disabled = true;
    enviarPassagemButton.textContent = "Enviando...";

    try {
        const response = await fetch(`${API_URL}/passagens/tecon`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(montarPassagem()),
        });
        const dados = await response.json();
        if (response.status === 401) {
            sessionStorage.removeItem("access_token");
            window.location.replace("./index.html");
            return;
        }
        if (!response.ok) {
            exibirMensagemEnvio(extrairMensagemErro(dados));
            return;
        }
        sessionStorage.setItem(
            "ultima_passagem",
            JSON.stringify({
                id: dados.id,
                mensagem: dados.mensagem,
                terminal: "Terminal TECON",
                data: document.getElementById("data").value,
                turno: document.getElementById("turno").value,
            })
        );
        window.location.href = "./confirmacao.html";
    } catch (error) {
        exibirMensagemEnvio("Não foi possível conectar ao servidor.");
    } finally {
        if (window.location.pathname.endsWith("tecon.html")) {
            enviarPassagemButton.disabled = false;
            enviarPassagemButton.textContent = "Enviar passagem de serviço";
        }
    }
});
