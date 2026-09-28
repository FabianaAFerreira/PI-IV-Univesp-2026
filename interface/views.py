from pathlib import Path

import joblib
import pandas as pd

from django.shortcuts import render


BASE_DIR = Path(__file__).resolve().parent.parent

MODELO_PATH = BASE_DIR / "modelo_xgboost_novo.pkl"

CSV_PATH = (
    BASE_DIR
    / "historico_rampa_cspvl_v6"
    / "historico_rampa_cspvl_v6.csv"
)

modelo = joblib.load(MODELO_PATH)


def inicio(request):

    dados = pd.read_csv(
        CSV_PATH,
        sep=";"
    )

    ultimo = dados.sort_values("data").iloc[-1]

    amostra = [[
        ultimo["temperatura_media_c"],
        ultimo["chuva_mm"],
        ultimo["vento_medio_kmh"],
        ultimo["vento_maximo_kmh"],
        ultimo["direcao_vento_dominante_graus"],
    ]]

    previsao = modelo.predict(amostra)[0]

    classes = {
        0: "ATENÇÃO",
        1: "INSEGURO",
        2: "SEGURO",
    }

    situacao = classes[int(previsao)]

    return render(
        request,
        'interface/inicio.html',
        {
            'situacao': situacao,
            'data': ultimo["data"],
            'temperatura': ultimo["temperatura_media_c"],
            'chuva': ultimo["chuva_mm"],
            'vento_medio': ultimo["vento_medio_kmh"],
            'vento_maximo': ultimo["vento_maximo_kmh"],
            'direcao_vento': ultimo["direcao_vento_dominante_graus"],
        }
    )