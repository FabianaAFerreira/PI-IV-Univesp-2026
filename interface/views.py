from pathlib import Path
from datetime import datetime, timedelta
from django.utils import timezone

import joblib
import pandas as pd
import requests

from django.shortcuts import render


BASE_DIR = Path(__file__).resolve().parent.parent

MODELO_PATH = BASE_DIR / "modelo" / "modelo_xgboost_novo.pkl"

URL_OPEN_METEO = "https://api.open-meteo.com/v1/forecast"

PARAMETROS_OPEN_METEO = {
    "latitude": -22.55,
    "longitude": -47.91,
    "daily": (
        "temperature_2m_mean,"
        "precipitation_sum,"
        "wind_speed_10m_mean,"
        "wind_speed_10m_max,"
        "wind_direction_10m_dominant"
    ),
    "timezone": "America/Sao_Paulo",
    "forecast_days": 1,
}

modelo = joblib.load(MODELO_PATH)


def inicio(request):
    hoje = timezone.localdate()
    data_selecionada = request.GET.get(
        "data",
        hoje.isoformat(),
    )

    contexto = {
        "erro": None,
        "data_selecionada": data_selecionada,
    }

    try:
        # Validar a data recebida pelo formulário.
        try:
            dia = datetime.strptime(
                data_selecionada,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            raise ValueError(
                "Data inválida. Selecione uma data válida."
            )

        # A previsão da API alcança até 16 dias à frente.
        if dia > hoje + timedelta(days=16):
            raise ValueError(
                "A previsão está disponível para até 16 dias à frente."
            )

        # Para datas recentes, usar a API de previsão.
        # Para datas mais antigas, usar a API de histórico.
        if dia >= hoje - timedelta(days=7):
            url_meteorologia = (
                "https://api.open-meteo.com/v1/forecast"
            )

            parametros = {
                "latitude": -22.55,
                "longitude": -47.91,
                "daily": (
                    "temperature_2m_mean,"
                    "precipitation_sum,"
                    "wind_speed_10m_mean,"
                    "wind_speed_10m_max,"
                    "wind_direction_10m_dominant"
                ),
                "timezone": "America/Sao_Paulo",
                "start_date": dia.isoformat(),
                "end_date": dia.isoformat(),
            }
        else:
            url_meteorologia = (
                "https://archive-api.open-meteo.com/v1/archive"
            )

            parametros = {
                "latitude": -22.55,
                "longitude": -47.91,
                "daily": (
                    "temperature_2m_mean,"
                    "precipitation_sum,"
                    "wind_speed_10m_mean,"
                    "wind_speed_10m_max,"
                    "wind_direction_10m_dominant"
                ),
                "timezone": "America/Sao_Paulo",
                "start_date": dia.isoformat(),
                "end_date": dia.isoformat(),
            }
        resposta = requests.get(
            url_meteorologia,
            params=parametros,
            timeout=20,
        )
        resposta.raise_for_status()

        dados_api = resposta.json()
        diario = dados_api["daily"]

        if not diario.get("time"):
            raise ValueError(
                "Não há dados meteorológicos disponíveis para essa data."
            )

        # Identificar a localidade pelas coordenadas retornadas.
        latitude = dados_api.get("latitude")
        longitude = dados_api.get("longitude")
        nome_local = "Itaqueri da Serra"

        try:
            resposta_local = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={
                    "lat": latitude,
                    "lon": longitude,
                    "format": "jsonv2",
                    "accept-language": "pt-BR",
                },
                headers={
                    "User-Agent": "ItaqueriAero/1.0"
                },
                timeout=(5, 10),
            )
            resposta_local.raise_for_status()

            endereco = resposta_local.json().get("address", {})
            nome_local = (
                endereco.get("village")
                or endereco.get("town")
                or endereco.get("city")
                or endereco.get("municipality")
                or endereco.get("county")
                or nome_local
            )
        except requests.RequestException as erro_local:
            print(
                "Não foi possível obter o nome da localidade:",
                erro_local,
            )

        entrada = {
            "data": diario["time"][0],
            "temperatura_media_c": diario["temperature_2m_mean"][0],
            "chuva_mm": diario["precipitation_sum"][0],
            "vento_medio_kmh": diario["wind_speed_10m_mean"][0],
            "vento_maximo_kmh": diario["wind_speed_10m_max"][0],
            "direcao_vento_dominante_graus": diario[
                "wind_direction_10m_dominant"
            ][0],
        }

        amostra = pd.DataFrame([{
            "temperatura_media_c": entrada["temperatura_media_c"],
            "chuva_mm": entrada["chuva_mm"],
            "vento_medio_kmh": entrada["vento_medio_kmh"],
            "vento_maximo_kmh": entrada["vento_maximo_kmh"],
            "direcao_vento_dominante_graus": entrada[
                "direcao_vento_dominante_graus"
            ],
        }])

        previsao = int(modelo.predict(amostra)[0])

        classes = {
            0: "ATENÇÃO",
            1: "INSEGURO",
            2: "SEGURO",
        }

        contexto.update({
            "nome_local": nome_local,
            "latitude": latitude,
            "longitude": longitude,
            "situacao": classes.get(
                previsao,
                f"Classe não identificada ({previsao})",
            ),
            "data": entrada["data"],
            "temperatura": entrada["temperatura_media_c"],
            "chuva": entrada["chuva_mm"],
            "vento_medio": entrada["vento_medio_kmh"],
            "vento_maximo": entrada["vento_maximo_kmh"],
            "direcao_vento": entrada[
                "direcao_vento_dominante_graus"
            ],
        })

    except (requests.RequestException, ValueError, KeyError, IndexError) as erro:
        print("Erro ao consultar os dados meteorológicos:", erro)
        contexto["erro"] = str(erro) or (
            "Não foi possível consultar os dados meteorológicos."
        )


    return render(
        request,
        "interface/inicio.html",
        contexto,
    )