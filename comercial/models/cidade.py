from django.db import models


class Cidade(models.Model):
    cidade = models.IntegerField("Cidade", primary_key=True)
    nome = models.CharField("Nome da Cidade", max_length=50, blank=False)
    estado = models.SmallIntegerField("Estado")
    uf = models.CharField("UF", max_length=2)
    cep_inicial = models.IntegerField("CEP Inicial", null=True)
    cep_final = models.IntegerField("CEP Final", null=True)
    estado_nome = models.CharField("Nome do Estado", max_length=50)
    ddd = models.SmallIntegerField("DDD", null=True)

    class Meta:
        db_table = "cidade"
        ordering = ["nome"]
        verbose_name = "cidade"
        verbose_name_plural = "cidades"

    def __str__(self):
        return self.nome