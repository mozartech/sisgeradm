from django.db import models
from django.utils import timezone

from .cliente import Cliente
from .fabrica import Fabrica
from .vendedor import Vendedor

'''
PARCELAS = [
    (1, '1 PARCELA'),
    (2, '2 PARCELAS'),
    (3, '3 PARCELAS'),
]
'''

SEMANAS = [
    (1, '1ª SEMANA'),
    (2, '2ª SEMANA'),
    (3, '3ª SEMANA'),
    (4, '4ª SEMANA'),
    (5, '5ª SEMANA'),
]

MESES = [
    (1, 'JANEIRO'),
    (2, 'FEVEREIRO'),
    (3, 'MARÇO'),
    (4, 'ABRIL'),
    (5, 'MAIO'),
    (6, 'JUNHO'),
    (7, 'JULHO'),
    (8, 'AGOSTO'),
    (9, 'SETEMBRO'),
    (10, 'OUTUBRO'),
    (11, 'NOVEMBRO'),
    (12, 'DEZEMBRO')
]


class Pedido(models.Model):
    data = models.DateField('Data')
    fabrica = models.ForeignKey(Fabrica, verbose_name='Fabrica', on_delete=models.PROTECT)
    vendedor = models.ForeignKey(Vendedor, verbose_name='Vendedor', on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente', on_delete=models.PROTECT)
    marcas = models.TextField('marcas', default='', blank=True)
    cadastro = models.DateTimeField('cadastro', blank=True, editable=False)
    credenciado = models.IntegerField('credenciado', null=True, editable=False)
    semana_numero = models.SmallIntegerField('semana', null=True, blank=True)
    prazos = models.CharField(max_length=15, default='', blank=True)
    #parcela = models.SmallIntegerField('parcela', choices=PARCELAS, default=3)
    #semana = models.SmallIntegerField('semana', choices=SEMANAS, default=1)
    embarque = models.SmallIntegerField('embarque', choices=SEMANAS, default=1)
    desconto = models.FloatField('desconto', default=0)
    qtde = models.SmallIntegerField('quantidade')
    valor = models.FloatField('valor')
    codigo_2 = models.CharField(max_length=15, default='', blank=True)
    codigo_3 = models.CharField(max_length=15, default='', blank=True)
    fatura_mes = models.SmallIntegerField('mês de faturamento', null=True, choices=MESES)
    
    class Meta:
        db_table = 'pedido'

    def save(self, *args, **kwargs):
        if not self.cadastro:
            self.cadastro = timezone.now()
        super().save(*args, **kwargs)

