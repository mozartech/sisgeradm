from os.path import splitext, join
import re

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from accounts.models import MyUser

from base.models import (
    PESSOA_TIPO, UF_SIGLA
)

from sisgeradm.storages import MediaStorage


def anexo(cliente, id, doc, filename):
    file_name = '{0}-{1}{2}'.format(id, doc, splitext(filename.lower())[1])
    folder_name = '{0}'.format(cliente)
    return join(folder_name, 'cliente', file_name)


def foto_1(instance, filename):
    return anexo(instance.credenciado, instance.id, 'foto_1', filename)


def foto_2(instance, filename):
    return anexo(instance.credenciado, instance.id, 'foto_2', filename)


def foto_3(instance, filename):
    return anexo(instance.credenciado, instance.id, 'foto_3', filename)


def foto_4(instance, filename):
    return anexo(instance.credenciado, instance.id, 'foto_4', filename)


class Canal(models.Model):
    nome = models.CharField('nome', max_length=20)
    credenciado = models.IntegerField('credenciado', null=True, editable=False)

    class Meta:
        db_table = "canal"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Marca(models.Model):
    nome = models.CharField('nome', max_length=50)
    ativo = models.BooleanField('ativo', null=True, default=True)
    credenciado = models.IntegerField('credenciado', null=True, editable=False)

    class Meta:
        db_table = 'marca'


class Grupo(models.Model):
    nome = models.CharField('nome', max_length=50)
    credenciado = models.IntegerField('credenciado', null=True, editable=False)
    
    class Meta:
        db_table = 'grupo'

    def __str__(self):
        return self.nome
        

class Segmento(models.Model):
    nome = models.CharField('nome', max_length=20)
    credenciado = models.IntegerField('credenciado', null=True, editable=False)

    class Meta:
        db_table = "segmento"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Status(models.Model):
    nome = models.CharField('nome', max_length=20)
    credenciado = models.IntegerField('credenciado', null=True, editable=False)

    class Meta:
        db_table = "status"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField('nome', max_length=100)
    fantasia = models.CharField('nome fantasia', default='', max_length=50, blank=True)
    pessoa = models.CharField('pessoa', max_length=2, choices=PESSOA_TIPO, default='PJ')
    codigo = models.CharField('código', default='', max_length=10, blank=True)
    email = models.EmailField('e-mail', max_length=254, default='', blank=True)
    instagram = models.CharField('instagram', max_length=50, default='', blank=True)
    inscricao_estadual = models.CharField('inscrição estadual', max_length=12, default='', blank=True)
    cnpj = models.CharField('cnpj', max_length=18, default='', blank=True)
    cpf = models.CharField('cpf', max_length=14, default='', blank=True)
    chave = models.CharField('chave', max_length=14, default='', editable=False)

    endereco_cep = models.CharField('cep', max_length=10, default='', blank=True)
    endereco_uf = models.CharField('uf', max_length=2, choices=UF_SIGLA, default='', blank=True)
    endereco_cidade = models.CharField('cidade', max_length=50, default='', blank=True)
    endereco_logradouro = models.CharField('logradouro', max_length=100, default='', blank=True)
    endereco_bairro = models.CharField('bairro', max_length=50, default='', blank=True)
    endereco_numero = models.CharField('número', max_length=20, default='', blank=True)

    ativo = models.BooleanField('ativo', null=True, default=True)
    status = models. ForeignKey(Status, verbose_name='Status', null=True, on_delete=models.PROTECT)
    fundacao = models.DateField('fundação', null=True, blank=True)
    segmento = models.ForeignKey(Segmento, verbose_name='Segmento', null=True, on_delete=models.PROTECT)
    grupo = models.ForeignKey(Grupo, verbose_name='Grupo', null=True, on_delete=models.PROTECT)
    canal = models.ForeignKey(Canal, verbose_name='Canal', null=True, on_delete=models.PROTECT)

    telefone_1 = models.CharField('telefone fixo', max_length=15, default='', blank=True)
    telefone_2 = models.CharField('telefone móvel', max_length=15, default='', blank=True)
    contatos = models.TextField('contatos', default='', blank=True)
    marcas = models.TextField('marcas', default='', blank=True)
    vendedores = models.TextField('vendedores', null=True, default='', blank=True)

    credenciado = models.IntegerField('credenciado', editable=False)
    usuario = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    cadastro = models.DateTimeField('cadastro', null=True, blank=True, editable=False)

    foto_1 = models.FileField(upload_to=foto_1, storage=MediaStorage, null=True, blank=True)
    foto_2 = models.FileField(upload_to=foto_2, storage=MediaStorage, null=True, blank=True)
    foto_3 = models.FileField(upload_to=foto_3, storage=MediaStorage, null=True, blank=True)
    foto_4 = models.FileField(upload_to=foto_4, storage=MediaStorage, null=True, blank=True)

    class Meta:
        db_table = 'cliente'
        constraints  = [
           models.UniqueConstraint(fields=['chave'], name='cliente_chave_idx'),
        ]

    @property
    def get_cnpj_cpf(self):

        if self.pessoa == 'PF':
            return self.cpf
        else:
            return self.cnpj

    @property
    def get_cnpj_cpf2(self):
        s = self.get_cnpj_cpf
        if s:
            s = s.replace('.', '').replace('-', '').replace('/','')
        return s

    @property
    def get_telefones(self):

        telefones = []

        if self.telefone_1:
            telefones.append(self.telefone_1)

        if self.telefone_2:
            telefones.append(self.telefone_2)
            
        return ' / '.join(telefones)

    def save(self, *args, **kwargs):

        s = self.cpf
        if s and len(s) == 11:
            self.cpf = s[:3]+'.'+s[3:6]+'.'+s[6:9]+'-'+s[9:11]

        s = self.cnpj
        if s and len(s) == 14:
            self.cnpj = s[0:2]+'.'+s[2:5]+'.'+s[5:8]+'/'+s[8:12]+'-'+s[12:14]

        s = self.inscricao_estadual
        if s and len(s) == 9:
            self.inscricao_estadual = s[0:2]+'.'+s[2:5]+'.'+s[5:8]+'-'+s[8]

        if self.pessoa == 'PF':
            self.chave = ''.join(re.findall(r'\d+', self.cpf))
            self.cnpj = ''
            self.inscricao_estadual = ''

        if self.pessoa == 'PJ':
            self.chave = ''.join(re.findall(r'\d+', self.cnpj))
            self.cpf = ''

        if not self.cadastro:
            self.cadastro = timezone.now()

        super().save(*args, **kwargs)


class ClienteMarca(models.Model):
    cliente = models.ForeignKey(Cliente, verbose_name='cliente', on_delete=models.CASCADE)
    marca_id = models.IntegerField(null=True)
    credenciado = models.IntegerField(null=True)

    class Meta:
        db_table = 'cliente_marca'

    def save(self, *args, **kwargs):
        self.credenciado = self.cliente.credenciado
        super().save(*args, **kwargs)


class ClienteVendedor(models.Model):
    cliente = models.ForeignKey(Cliente, verbose_name='cliente', on_delete=models.CASCADE)
    vendedor_id = models.IntegerField(null=True)
    credenciado = models.IntegerField(null=True)

    class Meta:
        db_table = 'cliente_vendedor'

    def save(self, *args, **kwargs):
        self.credenciado = self.cliente.credenciado
        super().save(*args, **kwargs)


def ClienteUpdateMarca(cliente):

    if cliente.marcas:
        lista = list(map(int, cliente.marcas.split(',')))
    else:
        lista = []

    for item in cliente.clientemarca_set.all():
        if not item.marca_id in lista:
            item.delete()

    marcas = []

    for item in cliente.clientemarca_set.all():
        marcas.append(item.marca_id)

    for marca_id in lista:
        if not marca_id in marcas:
            item = ClienteMarca()
            item.cliente = cliente
            item.marca_id = marca_id
            item.save()    


def ProcessaClienteUpdateMarca():
    for cliente in Cliente.objects.all():
        ClienteUpdateMarca(cliente)


def ClienteUpdateVendedor(cliente):

    if cliente.vendedores:
        lista = list(map(int, cliente.vendedores.split(',')))
    else:
        lista = []

    for item in cliente.clientevendedor_set.all():
        if not item.vendedor_id in lista:
            item.delete()

    vendedores = []

    for item in cliente.clientevendedor_set.all():
        vendedores.append(item.vendedor_id)

    for vendedor_id in lista:
        if not vendedor_id in vendedores:
            item = ClienteVendedor()
            item.cliente = cliente
            item.vendedor_id = vendedor_id
            item.save()


def ProcessaClienteUpdateVendedor():
    for cliente in Cliente.objects.all():
        ClienteUpdateVendedor(cliente)


@receiver(post_save, sender=Cliente, dispatch_uid="update_cliente")
def update_cliente(sender, instance, **kwargs):
    ClienteUpdateMarca(instance)
    ClienteUpdateVendedor(instance)
