const API_URL = "http://127.0.0.1:8000";
const listaEquipe = document.getElementById("lista-equipe");
const adicionarMembroButton = document.getElementById("adicionar-membro");
const listaLinhas = document.getElementById("lista-linhas");
const linhasBrisamar = ["16", "18", "20", "22", "24", "26", "28", "30"];
const mobileOpcoes = document.querySelectorAll('input[name="mobile_utilizado"]');
const campoJustificativaMobile = document.getElementById(
    "campo-justificativa-mobile"
);
const mobileJustificativaInput = document.getElementById("mobile-justificativa");
const listaRadios = document.getElementById("lista-radios");
const radiosVazio = document.getElementById("radios-vazio");
const adicionarRadioButton = document.getElementById("adicionar-radio");
const formularioBrisamar = document.getElementById("formulario-brisamar");
const enviarPassagemButton = document.getElementById("enviar-passagem");
const mensagemEnvio = document.getElementById("mensagem-envio");
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

function atualizarEstadoRadios() {
    radiosVazio.hidden = listaRadios.children.length > 0;
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

function atualizarOrdemRadios() {
    listaRadios.querySelectorAll(".item-radio").forEach(function (radio, indice) {
        radio.querySelector(".ordem-radio").textContent = indice + 1;
    });
}

adicionarRadioButton.addEventListener("click", criarCampoRadio);
atualizarEstadoRadios();

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
            const posicao = linha.querySelector('[name="linha_sup_inf"]');
            return {
                codigo_linha: linha.dataset.codigoLinha,
                veiculos: valorOuNulo(
                    linha.querySelector('[name="linha_veiculos"]').value
                ),
                sup_inf: posicao ? valorOuNulo(posicao.value) : null,
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

function montarPassagem() {
    const mobileSelecionado = formularioBrisamar.querySelector(
        '[name="mobile_utilizado"]:checked'
    );
    const mobileUtilizado = mobileSelecionado.value === "true";

    return {
        data: document.getElementById("data").value,
        turno: document.getElementById("turno").value,
        observacoes: valorOuNulo(document.getElementById("observacoes").value),
        relatorio_ocorrencias: valorOuNulo(
            document.getElementById("relatorio-ocorrencias").value
        ),
        mobile_utilizado: mobileUtilizado,
        mobile_justificativa: mobileUtilizado
            ? null
            : valorOuNulo(mobileJustificativaInput.value),
        equipe: montarEquipe(),
        ocupacoes_linhas: montarOcupacoesLinhas(),
        detalhe: {
            radios_operantes: Number(document.getElementById("radios-operantes").value),
            radios_inoperantes: Number(
                document.getElementById("radios-inoperantes").value
            ),
            baterias: Number(document.getElementById("baterias").value),
            carregadores: Number(document.getElementById("carregadores").value),
            eots_disponiveis: valorOuNulo(
                document.getElementById("eots-disponiveis").value
            ),
            eots_avariados: valorOuNulo(
                document.getElementById("eots-avariados").value
            ),
        },
        radios_utilizados: montarRadiosUtilizados(),
    };
}

function exibirMensagemEnvio(texto, tipo) {
    mensagemEnvio.textContent = texto;
    mensagemEnvio.className = tipo;
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

formularioBrisamar.addEventListener("submit", async function (event) {
    event.preventDefault();
    exibirMensagemEnvio("", "");
    enviarPassagemButton.disabled = true;
    enviarPassagemButton.textContent = "Enviando...";

    try {
        const response = await fetch(`${API_URL}/passagens/brisamar`, {
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
            exibirMensagemEnvio(extrairMensagemErro(dados), "erro");
            return;
        }

        sessionStorage.setItem(
            "ultima_passagem",
            JSON.stringify({
                id: dados.id,
                mensagem: dados.mensagem,
                terminal: "Pátio Brisamar",
                data: document.getElementById("data").value,
                turno: document.getElementById("turno").value,
            })
        );
        window.location.href = "./confirmacao.html";
    } catch (error) {
        exibirMensagemEnvio("Não foi possível conectar ao servidor.", "erro");
    } finally {
        if (window.location.pathname.endsWith("brisamar.html")) {
            enviarPassagemButton.disabled = false;
            enviarPassagemButton.textContent = "Enviar passagem de serviço";
        }
    }
});
