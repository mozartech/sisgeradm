from django.db import models


class Contato(models.Model):
    nome = models.CharField('nome', max_length=50)
    funcao = models.CharField('função', max_length=50, default='', blank=True)
    nascimento = models.DateField('Data de nascimento', null=True)
    email = models.EmailField('e-mail', max_length=254, default='', blank=True)
    telefone1 = models.CharField('telefone móvel', max_length=15, default='', blank=True)
    telefone2 = models.CharField('telefone fixo', max_length=15, default='', blank=True)
    empresa = models.CharField('empresa', max_length=50, default='', blank=True)
    observacao = models.TextField('observação', default='', null=True, blank=True)    
    credenciado = models.IntegerField('credenciado', null=True, editable=False)

    class Meta:
        db_table = "contato"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    @property
    def get_telefones(self):

        telefones = []

        if self.telefone1:
            telefones.append(self.telefone1)

        if self.telefone2:
            telefones.append(self.telefone2)
            
        return ' / '.join(telefones)        