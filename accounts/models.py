import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from base.models import Credenciado

USER_ADMINISTRADOR = 0       # administrador do sistema
USER_SUPER = 1               # usuário especial do credenciado
USER_COMUM = 2               # usuário comum do credenciado
USER_REPRESENTANTE = 98      # usuário do proprietário
USER_PROPRIETARIO = 99       # dono da plataforma

USER_PERFIL = [
    (USER_ADMINISTRADOR, 'ADMINISTRADOR'),    # todas as permissões
    (USER_SUPER, 'SUPER USUÁRIO'),            # todas as permissões
    (USER_COMUM, 'USUÁRIO'),
    (USER_REPRESENTANTE, 'REPRESENTANTE'),    # todas as permissões
    (USER_PROPRIETARIO, 'PROPRIETARIO'),      # todas as permissões
]

USER_SIGLA = [
    (USER_ADMINISTRADOR, 'A'),
    (USER_SUPER, 'S'),
    (USER_COMUM, 'U'),
    (USER_REPRESENTANTE, 'R'),
    (USER_PROPRIETARIO, 'D'),  # dono
]

TEMAS = [
    ("", "Claro"),
    ("theme-dark", "Escuro"),
]

LAYOUTS = [
    ("", "Padrão"),
    ("condensado", "Condensado"),
]

FLUIDS = [
    ('', 'Não'),
    ('layout-fluid', 'Sim'),
]

STICKYS = [
    ("", "Não fixar"),
    ("sticky-top", "Fixar" )
]

NAV_COLORS = [
    ("", "Transparente"),
    ("navbar-light", "Claro"),
    ("navbar-dark", "Escuro"),
]


class MyUser(AbstractUser):
    foto = models.ImageField("Foto", null=True, blank=True)
    tema = models.CharField("Tema", max_length=50, choices=TEMAS, blank=True)
    layout = models.CharField("Layout", max_length=50, choices=LAYOUTS, default="", blank=True)
    fluid = models.CharField("Fluido", max_length=50, choices=FLUIDS, default="", blank=True)
    credenciado = models.ForeignKey(Credenciado, null=True, on_delete=models.RESTRICT, blank=True)
    telefone = models.CharField("Telefone", max_length=20, default="", blank=True)
    nav_sticky = models.CharField("Fixação do Menu", max_length=50, choices=STICKYS, default="", blank=True)
    nav_color = models.CharField("Cor do Menu", max_length=50, null=True, choices=NAV_COLORS, default="navbar-light", blank=True)
    perfil = models.IntegerField("perfil", choices=USER_PERFIL, null=True, default=USER_COMUM)

    @property
    def has_perm_user(self):
        '''
        Indica que o usuário tem permissão para acessar o cadastro de usuários
        '''
        return self.perfil == USER_SUPER or self.perfil == USER_ADMINISTRADOR

    @property
    def has_perm_cliente(self):
        '''
        Indica se o usuário tem permissão para acessar o cadastro de clientes
        '''
        return self.perfil in [USER_PROPRIETARIO, USER_REPRESENTANTE, USER_ADMINISTRADOR]

    @property
    def has_super(self):
        '''
        Indica que o usuário tem o perfil de SUPER_USUARIO
        '''
        return self.perfil == USER_SUPER

    @property
    def has_cadastro_editar(self):
        '''
        Indica que o usuário possui permissão para alterar os cadastros básicos
        '''
        return self.perfil in [USER_SUPER, USER_ADMINISTRADOR, USER_REPRESENTANTE, USER_COMUM]
    
    @property
    def has_perm_cadastro_editar(self):
        '''
        Indica que o usuário possui permissão para alterar os cadastros básicos
        '''
        return self.perfil in [USER_SUPER, USER_ADMINISTRADOR, USER_REPRESENTANTE, USER_COMUM]

    @property
    def perfil_nome(self):
        if self.perfil is not None:
            for i, s in USER_PERFIL:
                if i == int(self.perfil):
                    return s
        return ''

    @property
    def perfil_sigla(self):
        if self.perfil is not None:
            for i, s in USER_SIGLA:
                if i == int(self.perfil):
                    return s
        return ''

    @property
    def sigla(self):
        s = ''
        if self.first_name:
            s = s + self.first_name[0]
        if self.last_name:
            s = s + self.last_name[0]
        return s

    class Meta:
        ordering = ['first_name']
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(uuid.uuid4())
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        self.email = self.email.lower()

        super().save(*args, **kwargs)
        self.groups.clear()
