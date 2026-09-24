from django.db import models

class LocalDeVoo(models.Model):
    nome = models.CharField(max_length= 120)
    cidade = models.CharField(max_length = 120, default = "São Pedro")
    estado = models.CharField(max_length = 2, default = "SP")
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude_metros = models.PositiveIntegerField(blank = True, null = True)

    def __str__(self):
        return f"{self.nome} ({self.cidade}/{self.estado})"

class HistoricoDiario(models.Model):
    class Fonte(models.TextChoices):
        CSPVL_OBSERVADO = "CSPVL_OBSERVADO", "Estação CSPVL (observado)"
        NASA_POWER_MERRA2 = "NASA_POWER_MERRA2", "NASA POWER (reanalise)"

    local = models.ForeignKey(LocalDeVoo, on_delete=models.CASCADE, related_name="historico_diario")
    data = models.DateField()
    fonte = models.CharField(max_length=30, choices=Fonte.choices)

    temperatura_media_c = models.FloatField(null= True, blank= True)
    temperatura_maxima_c = models.FloatField(null= True, blank= True)
    hora_maxima = models.TimeField(null= True, blank= True)
    temperatura_minima_c = models.FloatField(null= True, blank= True)
    hora_minima = models.TimeField(null= True, blank= True)

    chuva_mm = models.FloatField(null= True, blank= True)
    umidade_media_pct = models.FloatField(null= True, blank= True)

    vento_medio_kmh = models.FloatField(null=True, blank= True)
    vento_maximo_kmh = models.FloatField(null= True, blank= True)
    hora_vento_maximo = models.TimeField(null= True, blank= True)
    direcao_vento_graus = models.FloatField(null= True, blank= True)

    url_origem = models.URLField(max_length = 500, blank= True)
    observacao = models.TextField(blank= True)

    class Meta:
        verbose_name = "Histórico diário"
        verbose_name_plural = "Histórico diário"
        ordering = ["-data"]
        unique_together = ("local", "data", "fonte")

    @property
    def classificacao_dia(self):
        chuva = self.chuva_mm or 0
        rajada = self.vento_maximo_kmh or 0

        if chuva > 2.0 or rajada > 35.0:
            return "risco"
        if (0.1 <= chuva <= 2.0) or (25.0 <= rajada <= 35.0):
            return "alerta"
        return "seguro"

    def __str__(self):
        return f"{self.local.nome} - {self.data} ({self.fonte})"