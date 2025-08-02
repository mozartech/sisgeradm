#from django.conf.urls import url
from django.urls import re_path

from . import views


app_name = 'accounts'

urlpatterns = [
    re_path(r'listar/$', views.UsuarioListarView, name='usuario_listar_view'),
    re_path(r'adicionar/$', views.UsuarioAdicionarView, name='usuario_adicionar_view'),
    re_path(r'alterar/(?P<pk>[0-9]+)/$', views.UsuarioEditarView, name='usuario_alterar_view'),
    re_path(r'visualizar/(?P<pk>[0-9]+)/$', views.UsuarioVisualizarView, name='usuario_visualizar_view'),
    re_path(r'apagar/(?P<pk>[0-9]+)/$', views.UsuarioApagarView, name='usuario_apagar_view'),
    re_path(r'perfil/$', views.UsuarioPerfilView, name='usuario_perfil_view'),

    re_path(r'credenciado/listar/$', views.CredenciadoListarView, name='credenciado_listar_view'),
    re_path(r'credenciado/adicionar/$', views.CredenciadoAdicionarView, name='credenciado_adicionar_view'),
    re_path(r'credenciado/ver/(?P<pk>[0-9]+)/$', views.CredenciadoVerView, name='credenciado_visualizar_view'),
    re_path(r'credenciado/alterar/(?P<pk>[0-9]+)/$', views.CredenciadoEditarView, name='credenciado_alterar_view'),
    re_path(r'credenciado/apagar/(?P<pk>[0-9]+)/$', views.CredenciadoApagarView, name='credenciado_apagar_view'),
    re_path(r'credenciado/ativar/(?P<pk>[0-9]+)/$', views.CredenciadoAtivarView, name='credenciado_ativar_view'),
    re_path(r'credenciado/perfil/$', views.CredenciadoPerfilView, name='credenciado_perfil_view'),

    re_path(r'administrador/listar/$', views.AdministradorListarView, name='administrador_listar_view'),
    re_path(r'administrador/adicionar/$', views.AdministradorAdicionarView, name='administrador_adicionar_view'),
    re_path(r'administrador/alterar/(?P<pk>[0-9]+)/$', views.AdministradorEditarView, name='administrador_alterar_view'),
    re_path(r'administrador/visualizar/(?P<pk>[0-9]+)/$', views.AdministradorVisualizarView, name='administrador_visualizar_view'),
    re_path(r'administrador/apagar/(?P<pk>[0-9]+)/$', views.AdministradorApagarView, name='administrador_apagar_view'),

    re_path(r'superusuario/listar/$', views.SuperUsuarioListarView, name='superusuario_listar_view'),
    re_path(r'superusuario/adicionar/$', views.SuperUsuarioAdicionarView, name='superusuario_adicionar_view'),
    re_path(r'superusuario/alterar/(?P<pk>[0-9]+)/$', views.SuperUsuarioEditarView, name='superusuario_alterar_view'),
    re_path(r'superusuario/visualizar/(?P<pk>[0-9]+)/$', views.SuperUsuarioVisualizarView, name='superusuario_visualizar_view'),
    re_path(r'superusuario/apagar/(?P<pk>[0-9]+)/$', views.SuperUsuarioApagarView, name='superusuario_apagar_view'),

]
