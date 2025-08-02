from django.db import models
from django.utils import timezone

from base.models import UF_SIGLA


class Fabrica(models.Model):
    nome = models.CharField('nome', max_length=100)
    cnpj = models.CharField('cnpj', max_length=18, default='', blank=True)
    contato = models.CharField('contato', max_length=50, default='', blank=True)
    email = models.EmailField('e-mail', max_length=254, default='', blank=True)
    telefone = models.CharField('telefone', max_length=15, default='', blank=True)
    endereco_cep = models.CharField('cep', max_length=10, default='', blank=True)
    endereco_uf = models.CharField('uf', max_length=2, choices=UF_SIGLA, default='', blank=True)
    endereco_cidade = models.CharField('cidade', max_length=50, default='', blank=True)
    endereco_logradouro = models.CharField('logradouro', max_length=100, default='', blank=True)
    endereco_bairro = models.CharField('bairro', max_length=50, default='', blank=True)
    endereco_numero = models.CharField('número', max_length=20, default='', blank=True)
    marcas = models.TextField('marcas', default='', blank=True)
    ativo = models.BooleanField('ativo', null=True, default=True)
    cadastro = models.DateTimeField('cadastro', null=True, blank=True, editable=False)
    credenciado = models.IntegerField('credenciado', null=True, editable=False)

    class Meta:
        db_table = 'fabrica'

    def __str__(self):
        return self.nome
        
    @property
    def get_cnpj_2(self):
        s = self.cnpj
        if s:
            s = s.replace('.', '').replace('-', '').replace('/','')
        return s

    def save(self, *args, **kwargs):
        
        s = self.cnpj

        if s and len(s) == 14:
            self.cnpj = s[0:2]+'.'+s[2:5]+'.'+s[5:8]+'/'+s[8:12]+'-'+s[12:14]

        if not self.cadastro:
            self.cadastro = timezone.now()

        super().save(*args, **kwargs)

