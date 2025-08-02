import simplejson

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from comercial.models import Contato, Cliente, Vendedor, Marca
from comercial.forms import ClienteForm
from base.models import CONTATO_TIPO
from base.utils import clear_text


@login_required
def ClienteAdicionarView(request):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:cliente_listar_view')

    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = ClienteForm(request=request)
    
    bairros = Cliente.objects.filter(credenciado=request.user.credenciado.pk).order_by('endereco_bairro').distinct('endereco_bairro')
    contatos = Contato.objects.filter(credenciado=request.user.credenciado.pk)
    vendedores = Vendedor.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    context = {
        'form': form,
        'acao': 'adicionar',
        'contatos': contatos,
        'vendedores': vendedores,
        'marcas': marcas,
        'bairros': bairros,
        'cliente_contatos': [],
        'cliente_vendedores': [],
        'cliente_marcas': [],
        'pretitle': 'Adicionar',
        'funcoes': CONTATO_TIPO,
        'return_url': url,
    }

    return render(request, "comercial/cliente_add.html", context)


@login_required
def ClienteEditarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:cliente_listar_view')

    cliente = get_object_or_404(Cliente, pk=pk)

    if cliente.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente, request=request, id=pk)
        if form.is_valid():
            cliente.save()
            return HttpResponseRedirect(url)
    else:
        form = ClienteForm(instance=cliente, request=request, id=pk)
   
    bairros = Cliente.objects.filter(
                    credenciado=request.user.credenciado.pk).order_by('endereco_bairro').distinct('endereco_bairro')

    contatos = Contato.objects.filter(credenciado=request.user.credenciado.pk)
    vendedores = Vendedor.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    cliente_contatos = []
    if cliente.contatos:
        cliente_contatos = list(map(int, cliente.contatos.split(',')))

    cliente_vendedores = []
    if cliente.vendedores:
        cliente_vendedores = list(map(int, cliente.vendedores.split(',')))

    cliente_marcas = []
    if cliente.marcas:
        cliente_marcas = list(map(int, cliente.marcas.split(',')))

    context = {
        'form': form,
        'acao': 'alterar',
        'bairros': bairros,
        'vendedores': vendedores,        
        'marcas': marcas,
        'contatos': contatos,
        'cliente_contatos': cliente_contatos,
        'cliente_vendedores': cliente_vendedores,
        'cliente_marcas': cliente_marcas,
        'funcoes': CONTATO_TIPO,
        'pretitle': 'Alterar',
        'return_url': url,
    }

    return render(request, "comercial/cliente_add.html", context)


@login_required
def ClienteApagarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    cliente = get_object_or_404(Cliente, pk=pk)

    if cliente.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:cliente_listar_view')

    if request.method == 'POST':
        cliente.delete()
        return HttpResponseRedirect(url)
    
    form = ClienteForm(instance=cliente)
   
    contatos = Contato.objects.filter(credenciado=request.user.credenciado.pk)
    vendedores = Vendedor.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    cliente_contatos = []
    if cliente.contatos:
        cliente_contatos = list(map(int, cliente.contatos.split(',')))

    cliente_vendedores = []
    if cliente.vendedores:
        cliente_vendedores = list(map(int, cliente.vendedores.split(',')))

    cliente_marcas = []
    if cliente.marcas:
        cliente_marcas = list(map(int, cliente.marcas.split(',')))

    context = {
        'form': form,
        'vendedores': vendedores,        
        'cliente_contatos': cliente_contatos,
        'cliente_vendedores': cliente_vendedores,
        'contatos': contatos,
        'marcas': marcas,        
        'cliente_marcas': cliente_marcas,
        'acao': 'apagar',
        'pretitle': 'Apagar',
        'return_url': url,
    }

    return render(request, "comercial/cliente_add.html", context)


@login_required
def ClienteVisualizarView(request, pk):

    cliente = get_object_or_404(Cliente, pk=pk)

    if cliente.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    form = ClienteForm(instance=cliente, request=request)
   
    contatos = Contato.objects.filter(credenciado=request.user.credenciado.pk)
    vendedores = Vendedor.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')   
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')


    cliente_contatos = []
    if cliente.contatos:
        cliente_contatos = list(map(int, cliente.contatos.split(',')))

    cliente_vendedores = []
    if cliente.vendedores:
        cliente_vendedores = list(map(int, cliente.vendedores.split(',')))

    cliente_marcas = []
    if cliente.marcas:
        cliente_marcas = list(map(int, cliente.marcas.split(',')))

    context = {
        'form': form,
        'contatos': contatos,
        'vendedores': vendedores,        
        'cliente_contatos': cliente_contatos,
        'cliente_vendedores': cliente_vendedores,
        'marcas': marcas,        
        'cliente_marcas': cliente_marcas,        
        'acao': 'visualizar',
        'pretitle': 'Visualizar',
        'return_url': reverse_lazy('comercial:cliente_listar_view'),
    }

    return render(request, "comercial/cliente_add.html", context)


def ClienteListar(request, queryset, title):

    context = {
        'queryset': queryset,
        'action_search': reverse_lazy('comercial:cliente_pesquisar_view'),
        'pretitle': title,
    }
    
    if request.user.has_perm_cadastro_editar:
        context['add_url'] = reverse_lazy('comercial:cliente_adicionar_view')

    return render(request, 'comercial/cliente_listar.html', context)


@login_required
def ClienteListarView(request):
    queryset = Cliente.objects.filter(credenciado=request.user.credenciado.pk)[:10]
    return ClienteListar(request, queryset, 'Recentes')
    

@login_required
def ClienteFiltrarView(request):

    queryset = Cliente.objects.filter(credenciado=request.user.credenciado.pk)

    
    context = {
        'queryset': queryset,
        'pretitle': 'Filtrados',
    }

    return render(request, 'comercial/cliente_filtrar.html', context)
    

def is_codigo_cliente(codigo):

    possui_numero = False
    possui_traco = False

    for c in codigo:
        if c.isnumeric():
            possui_numero = True
        elif c == '-':
            possui_traco = True
    
    return len(codigo) < 11 and possui_numero and possui_traco


def is_telefone(codigo):

    lista = codigo.split('-')

    return len(lista) == 2 and lista[0].isnumeric() and lista[1].isnumeric() and \
           len(lista[0]) in [4, 5] and len(lista[1]) == 4
    
    
@login_required
def ClientePesquisarView(request):

    if request.method != 'GET' or not request.GET.get('q'):
        return HttpResponseRedirect(reverse_lazy('comercial:cliente_listar_view'))

    search = request.GET.get('q')
    search = search.strip()

    queryset = Cliente.objects.filter(credenciado=request.user.credenciado.pk)

    if len(search) == 14 and search[3] == '.' and search[7] == '.' and search[11] == '-':  # CPF
        queryset = queryset.filter(cpf=search)

    elif len(search) == 11 and search.isnumeric():  # CPF
        search = search[0:3]+'.'+search[3:6]+'.'+search[6:9]+'-'+search[9:11]
        queryset = queryset.filter(cpf=search)

    elif len(search) == 18 and (search[2]+search[6]+search[10]+search[15]) == '../-':  # CNPJ
        queryset = queryset.filter(cnpj=search)

    elif len(search) == 14 and search.isnumeric():  # CNPJ
        search = search[0:2]+'.'+search[2:5]+'.'+search[5:8]+'/'+search[8:12]+'-'+search[12:]
        queryset = queryset.filter(cnpj=search)
    
    elif '@' in search:
        queryset = queryset.filter(email=search.lower())

    elif is_telefone(search):
        queryset = queryset.filter( Q(telefone_1__contains=search) | Q(telefone_2__contains=search) )

    elif is_codigo_cliente(search):
        if search[-1] == '-':
            queryset = queryset.filter(codigo__startswith=search)
        else:
            queryset = queryset.filter(codigo=search)

    else:
        search = search.upper()
        if '*' in search:
            search = clear_text(search.replace('*', ''))
            queryset = queryset.filter(nome__contains=search)
        else:
            search = clear_text(search)
            queryset = queryset.filter(nome__startswith=search)

    return ClienteListar(request, queryset, 'Encontrados')


@login_required
def ClienteProcurarView(request):

    clientes = []

    if request.method != 'GET':
        content = simplejson.dumps(clientes)
        return HttpResponse(content, content_type='application/json')

    if request.GET.get('q'):
        search = request.GET.get('q').upper()

    queryset = Cliente.objects.filter(credenciado=request.user.credenciado.pk)

    if request.GET.get('pk'):
        queryset = queryset.filter(pk=request.GET.get('pk'))
        
    elif len(search) == 14 and search[3] == '.' and search[7] == '.' and search[11] == '-':  # CPF
        queryset = queryset.filter(cpf=search)
    elif len(search) == 11 and search.isnumeric():  # CPF
        search = search[0:3]+'.'+search[3:6]+'.'+search[6:9]+'-'+search[9:11]
        queryset = queryset.filter(cpf=search)
    else:
        if '*' in search:
            search = clear_text(search.replace('*', ''))
            queryset = queryset.filter(nome__contains=search)
        else:
            search = clear_text(search)
            queryset = queryset.filter(nome__startswith=search)

    for cliente in queryset.all():
        clientes.append({
            'pk': cliente.pk, 
            'nome': cliente.nome,
            'cnpj_cpf': cliente.get_cnpj_cpf,
            'endereco_cidade': cliente.endereco_cidade
        })

    content = simplejson.dumps(clientes)
    
    return HttpResponse(content, content_type='application/json')


@login_required
def ClienteProcurarNomeView(request):

    clientes = []

    if request.method != 'GET':
        content = simplejson.dumps(clientes)
        return HttpResponse(content, content_type='application/json')

    queryset = Cliente.objects.filter(credenciado=request.user.credenciado.pk)

    search = clear_text(request.GET.get('q').upper())
    queryset = queryset.filter(nome=search)

    for cliente in queryset.all():
        clientes.append({'pk': cliente.pk, 
                         'nome': cliente.nome})

    content = simplejson.dumps(clientes)

    return HttpResponse(content, content_type='application/json')
