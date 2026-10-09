const CONFIG = {
    LATITUDE: -23.5505,
    LONGITUDE: -46.6333,
    MAX_VENTO_KMH: 25,
    MAX_RAJADA_KMH: 35,
    INTERVALO_ATUALIZACAO_MS: 10000,
};

const API_URL = `https://api.open-meteo.com/v1/forecast?latitude=${CONFIG.LATITUDE}&longitude=${CONFIG.LONGITUDE}&current=wind_speed_10m,wind_gusts_10m,cloud_cover&wind_speed_unit=kmh`;

// Cache dos elementos do DOM para evitar buscas repetitivas
const domElements = {};

function inicializarDOM() {
    domElements.ventoMedio = document.getElementById('vento-medio');
    domElements.ventoMaximo = document.getElementById('vento-maximo');
    domElements.nuvens = document.getElementById('nuvens');
    domElements.card = document.getElementById('card-situacao');
    domElements.texto = document.getElementById('texto-situacao');
}

async function buscarDadosSatelite() {
    try {
        const response = await fetch(API_URL);
        
        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
        
        const { current } = await response.json();
        
        atualizarInterface(current.wind_speed_10m, current.wind_gusts_10m, current.cloud_cover);
    } catch (error) {
        console.error("Erro ao sincronizar dados meteorológicos:", error);
    }
}

function atualizarInterface(vento, rajada, nuvens) {
    if (domElements.ventoMedio) domElements.ventoMedio.textContent = vento;
    if (domElements.ventoMaximo) domElements.ventoMaximo.textContent = rajada;
    if (domElements.nuvens) domElements.nuvens.textContent = nuvens;

    if (!domElements.card || !domElements.texto) return;

    const isCondicaoSegura = vento < CONFIG.MAX_VENTO_KMH && rajada < CONFIG.MAX_RAJADA_KMH;

    if (isCondicaoSegura) {
        domElements.card.className = "situacao seguro";
        domElements.texto.textContent = "SEGURO (✅ Favorável)";
    } else {
        domElements.card.className = "situacao risco";
        domElements.texto.textContent = "INSEGURO (❌ Perigoso)";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    inicializarDOM();
    buscarDadosSatelite();
    setInterval(buscarDadosSatelite, CONFIG.INTERVALO_ATUALIZACAO_MS);
});
