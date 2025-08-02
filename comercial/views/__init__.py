
from .gerencial import (
   GerencialDashboard,
   GerencialClienteCanal,
   GerencialClienteSegmento,
   GerencialClienteStatus,
   GerencialClienteGrupo,
   GerencialClienteMarca,
   GerencialClienteVendedor,
   GerencialPesquisaCliente,
   GerencialResumoVenda
)

from .cidade import (
    CidadeUFView, CidadeView,
)

from .cliente import (
    ClienteAdicionarView, ClienteEditarView,
    ClienteVisualizarView, ClienteApagarView,
    ClienteListarView, ClientePesquisarView,
    ClienteProcurarView, ClienteProcurarNomeView,
    ClienteFiltrarView,
)

from .contato import (
    ContatoAdicionarView, ContatoEditarView,
    ContatoVisualizarView, ContatoApagarView,
    ContatoListarView, ContatoAdicionarJson
)
from .canal import (
    CanalAdicionarView, CanalEditarView,
    CanalVisualizarView, CanalApagarView,
    CanalListarView
)

from .fabrica import (
    FabricaAdicionarView, FabricaEditarView,
    FabricaVisualizarView, FabricaApagarView,
    FabricaListarView, FabricaPesquisarView,
    FabricaProcurarView, FabricaProcurarNomeView
)

from .grupo import (
    GrupoAdicionarView, GrupoEditarView,
    GrupoVisualizarView, GrupoApagarView, GrupoListarView
)

from .marca import (
    MarcaAdicionarView, MarcaEditarView,
    MarcaVisualizarView, MarcaApagarView, MarcaListarView
)

from .pedido import (
    PedidoAdicionarView, PedidoEditarView,
    PedidoVisualizarView, PedidoApagarView,
    PedidoPesquisarView, PedidoListarView
)

from .segmento import (
    SegmentoAdicionarView, SegmentoEditarView,
    SegmentoVisualizarView, SegmentoApagarView,
    SegmentoListarView
)

from .status import (
    StatusAdicionarView, StatusEditarView,
    StatusVisualizarView, StatusApagarView, StatusListarView
)

from .vendedor import (
    VendedorAdicionarView, VendedorEditarView,
    VendedorVisualizarView, VendedorApagarView, VendedorListarView
)
