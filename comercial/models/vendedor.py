from django.db import models

from .cliente import Marca
from .base import BANCOS


class Vendedor(models.Model):
    nome = models.CharField('nome', max_length=100)
    nascimento = models.DateField('data de nascimento', null=True, blank=True)
    cpf = models.CharField('cpf', max_length=14, default='', blank=True)
    email = models.EmailField('e-mail', max_length=254, default='', blank=True)
    telefone = models.CharField('telefone', max_length=15, default='', blank=True)
    banco = models.CharField('banco', max_length=3, choices=BANCOS, default='', blank=True)
    agencia = models.CharField('agência', max_length=4, default='', blank=True)
    conta = models.CharField('conta', max_length=10, default='', blank=True)
    conta_dv = models.CharField('DV', max_length=1, default='', blank=True)
    pix = models.CharField('chave pix', max_length=50, default='', blank=True)
    ativo = models.BooleanField('ativo', null=True, default=True)
    credenciado = models.IntegerField('credenciado', null=True, editable=False)

    class Meta:
        db_table = 'vendedor'

    def __str__(self):
        return self.nome


class VendedorMarca(models.Model):
    vendedor = models.ForeignKey(Vendedor, verbose_name='vendedor', on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, verbose_name='marca', on_delete=models.CASCADE)

    class Meta:
        db_table = 'vendedor_marca'