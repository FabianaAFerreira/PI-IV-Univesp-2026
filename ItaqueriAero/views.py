from django.shortcuts import render
from .models import LocalDeVoo, HistoricoDiario

def dashboard(request):
    local = LocalDeVoo.objects.first()

    registros = HistoricoDiario.objects.filter(local=local)

    registro_id = request.GET.get("registro")

    if registro_id:
        registro = registros.filter(id=registro_id).first()
    else:
        registro = registros.first()

    return render(request, "ItaqueriAero/dashboard.html", {
        "local": local,
        "registro": registro,
        "registros": registros,
    })

def historico(request):
    local = LocalDeVoo.objects.first()
    historico = HistoricoDiario.objects.filter(local=local)

    return render(request, "ItaqueriAero/historico.html", {
        "local": local,
        "historico": historico,
    })