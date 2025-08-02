from django.urls import re_path

from . import views

app_name = 'comercial'

urlpatterns = [
    re_path(r'gerencial/pesquisa_cliente/$', views.GerencialPesquisaCliente, name='gerencial_pesquisa_cliente_view'),
    re_path(r'gerencial/dashboard/$', views.GerencialDashboard, name='gerencial_dashboard_view'),
    re_path(r'gerencial/cliente/canal/(?P<codigo>[0-9]+)/$', views.GerencialClienteCanal, name='gerencial_cliente_canal_view'),
    re_path(r'gerencial/cliente/segmento/(?P<codigo>[0-9]+)/$', views.GerencialClienteSegmento, name='gerencial_cliente_segmento_view'),
    re_path(r'gerencial/cliente/status/(?P<codigo>[0-9]+)/$', views.GerencialClienteStatus, name='gerencial_cliente_status_view'),
    re_path(r'gerencial/cliente/grupo/(?P<codigo>[0-9]+)/$', views.GerencialClienteGrupo, name='gerencial_cliente_grupo_view'),
    re_path(r'gerencial/cliente/vendedor/(?P<codigo>[0-9]+)/$', views.GerencialClienteVendedor, name='gerencial_cliente_vendedor_view'),
    re_path(r'gerencial/cliente/marca/(?P<codigo>[0-9]+)/$', views.GerencialClienteMarca, name='gerencial_cliente_marca_view'),
    re_path(r'gerencial/resumo/venda/(?P<ano>[0-9]+)/$', views.GerencialResumoVenda, name='gerencial_resumo_venda_view'),    

    re_path(r'cliente/filtrar/$', views.ClienteListarView, name='cliente_filtrar_view'),
    re_path(r'cliente/listar/$', views.ClienteListarView, name='cliente_listar_view'),
    re_path(r'cliente/pesquisar', views.ClientePesquisarView, name='cliente_pesquisar_view'),
    re_path(r'cliente/adicionar/$', views.ClienteAdicionarView, name='cliente_adicionar_view'),
    re_path(r'cliente/alterar/(?P<pk>[0-9]+)/$', views.ClienteEditarView, name='cliente_alterar_view'),
    re_path(r'cliente/visualizar/(?P<pk>[0-9]+)/$', views.ClienteVisualizarView, name='cliente_visualizar_view'),
    re_path(r'cliente/apagar/(?P<pk>[0-9]+)/$', views.ClienteApagarView, name='cliente_apagar_view'),
    re_path(r'cliente/procurar', views.ClienteProcurarView, name='cliente_procurar_view'),
    re_path(r'cliente/procurarnome', views.ClienteProcurarNomeView, name='cliente_procurar_nome_view'),

    re_path(r'contato/listar/$', views.ContatoListarView, name='contato_listar_view'),
    re_path(r'contato/adicionar/$', views.ContatoAdicionarView, name='contato_adicionar_view'),
    re_path(r'contato/alterar/(?P<pk>[0-9]+)/$', views.ContatoEditarView, name='contato_alterar_view'),
    re_path(r'contato/visualizar/(?P<pk>[0-9]+)/$', views.ContatoVisualizarView, name='contato_visualizar_view'),
    re_path(r'contato/apagar/(?P<pk>[0-9]+)/$', views.ContatoApagarView, name='contato_apagar_view'),
    re_path(r'contato/add/$', views.ContatoAdicionarJson, name='contato_adicionar_json'),

    re_path(r'canal/listar/$', views.CanalListarView, name='canal_listar_view'),
    re_path(r'canal/adicionar/$', views.CanalAdicionarView, name='canal_adicionar_view'),
    re_path(r'canal/alterar/(?P<pk>[0-9]+)/$', views.CanalEditarView, name='canal_alterar_view'),
    re_path(r'canal/visualizar/(?P<pk>[0-9]+)/$', views.CanalVisualizarView, name='canal_visualizar_view'),
    re_path(r'canal/apagar/(?P<pk>[0-9]+)/$', views.CanalApagarView, name='canal_apagar_view'),

    re_path(r'fabrica/listar/$', views.FabricaListarView, name='fabrica_listar_view'),
    re_path(r'fabrica/pesquisar', views.FabricaPesquisarView, name='fabrica_pesquisar_view'),
    re_path(r'fabrica/adicionar/$', views.FabricaAdicionarView, name='fabrica_adicionar_view'),
    re_path(r'fabrica/alterar/(?P<pk>[0-9]+)/$', views.FabricaEditarView, name='fabrica_alterar_view'),
    re_path(r'fabrica/visualizar/(?P<pk>[0-9]+)/$', views.FabricaVisualizarView, name='fabrica_visualizar_view'),
    re_path(r'fabrica/apagar/(?P<pk>[0-9]+)/$', views.FabricaApagarView, name='fabrica_apagar_view'),
    re_path(r'fabrica/procurar', views.FabricaProcurarView, name='fabrica_procurar_view'),
    re_path(r'fabrica/procurarnome', views.FabricaProcurarNomeView, name='fabrica_procurar_nome_view'),

    re_path(r'pedido/listar/$', views.PedidoListarView, name='pedido_listar_view'),
    re_path(r'pedido/pesquisar', views.PedidoPesquisarView, name='pedido_pesquisar_view'),
    re_path(r'pedido/adicionar/$', views.PedidoAdicionarView, name='pedido_adicionar_view'),
    re_path(r'pedido/alterar/(?P<pk>[0-9]+)/$', views.PedidoEditarView, name='pedido_alterar_view'),
    re_path(r'pedido/visualizar/(?P<pk>[0-9]+)/$', views.PedidoVisualizarView, name='pedido_visualizar_view'),
    re_path(r'pedido/apagar/(?P<pk>[0-9]+)/$', views.PedidoApagarView, name='pedido_apagar_view'),


    re_path(r'grupo/listar/$', views.GrupoListarView, name='grupo_listar_view'),
    re_path(r'grupo/adicionar/$', views.GrupoAdicionarView, name='grupo_adicionar_view'),
    re_path(r'grupo/alterar/(?P<pk>[0-9]+)/$', views.GrupoEditarView, name='grupo_alterar_view'),
    re_path(r'grupo/visualizar/(?P<pk>[0-9]+)/$', views.GrupoVisualizarView, name='grupo_visualizar_view'),
    re_path(r'grupo/apagar/(?P<pk>[0-9]+)/$', views.GrupoApagarView, name='grupo_apagar_view'),

    re_path(r'marca/listar/$', views.MarcaListarView, name='marca_listar_view'),
    re_path(r'marca/adicionar/$', views.MarcaAdicionarView, name='marca_adicionar_view'),
    re_path(r'marca/alterar/(?P<pk>[0-9]+)/$', views.MarcaEditarView, name='marca_alterar_view'),
    re_path(r'marca/visualizar/(?P<pk>[0-9]+)/$', views.MarcaVisualizarView, name='marca_visualizar_view'),
    re_path(r'marca/apagar/(?P<pk>[0-9]+)/$', views.MarcaApagarView, name='marca_apagar_view'),
    
    re_path(r'segmento/listar/$', views.SegmentoListarView, name='segmento_listar_view'),
    re_path(r'segmento/adicionar/$', views.SegmentoAdicionarView, name='segmento_adicionar_view'),
    re_path(r'segmento/alterar/(?P<pk>[0-9]+)/$', views.SegmentoEditarView, name='segmento_alterar_view'),
    re_path(r'segmento/visualizar/(?P<pk>[0-9]+)/$', views.SegmentoVisualizarView, name='segmento_visualizar_view'),
    re_path(r'segmento/apagar/(?P<pk>[0-9]+)/$', views.SegmentoApagarView, name='segmento_apagar_view'),

    re_path(r'status/listar/$', views.StatusListarView, name='status_listar_view'),
    re_path(r'status/adicionar/$', views.StatusAdicionarView, name='status_adicionar_view'),
    re_path(r'status/alterar/(?P<pk>[0-9]+)/$', views.StatusEditarView, name='status_alterar_view'),
    re_path(r'status/visualizar/(?P<pk>[0-9]+)/$', views.StatusVisualizarView, name='status_visualizar_view'),
    re_path(r'status/apagar/(?P<pk>[0-9]+)/$', views.StatusApagarView, name='status_apagar_view'),

    re_path(r'vendedor/listar/$', views.VendedorListarView, name='vendedor_listar_view'),
    re_path(r'vendedor/adicionar/$', views.VendedorAdicionarView, name='vendedor_adicionar_view'),
    re_path(r'vendedor/alterar/(?P<pk>[0-9]+)/$', views.VendedorEditarView, name='vendedor_alterar_view'),
    re_path(r'vendedor/visualizar/(?P<pk>[0-9]+)/$', views.VendedorVisualizarView, name='vendedor_visualizar_view'),
    re_path(r'vendedor/apagar/(?P<pk>[0-9]+)/$', views.VendedorApagarView, name='vendedor_apagar_view'),
    
    re_path(r'cidade/$', views.CidadeView, name='cidadeview'),
    re_path(r'cidade/(?P<uf>[A-Z,a-z]+)/$', views.CidadeUFView, name='cidadeUFview'),

]