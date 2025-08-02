from datetime import date
import simplejson

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from comercial.models import Fabrica, Pedido, Marca
from comercial.forms import PedidoForm
from base.utils import clear_text


@login_required
def PedidoAdicionarView(request):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:pedido_listar_view')

    if request.method == 'POST':
        form = PedidoForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = PedidoForm(request=request)
    
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    fabricas = Fabrica.objects.filter(
        credenciado=request.user.credenciado.pk,
        ativo=True
    ).order_by('nome')

    context = {
        'form': form,
        'acao': 'adicionar',
        'pedido_marcas': [],
        'fabricas': fabricas,
        'marcas': marcas,
        'pretitle': 'Adicionar',
        'return_url': url,
    }

    return render(request, "comercial/pedido_add.html", context)


@login_required
def PedidoEditarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:pedido_listar_view')

    pedido = get_object_or_404(Pedido, pk=pk)

    if pedido.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido, request=request, id=pk)
        if form.is_valid():
            pedido.save()
            return HttpResponseRedirect(url)
    else:
        form = PedidoForm(instance=pedido, request=request, id=pk)
   
    fabricas = Fabrica.objects.filter(
        credenciado=request.user.credenciado.pk
    ).order_by('nome')

    marcas = Marca.objects.filter(
        credenciado=request.user.credenciado.pk
    ).order_by('nome')

    pedido_marcas = []

    if pedido.marcas:
        pedido_marcas = list(map(int, pedido.marcas.split(',')))

    context = {
        'form': form,
        'acao': 'alterar',
        'fabricas': fabricas,
        'marcas': marcas,
        'pedido_marcas': pedido_marcas,
        'pretitle': 'Alterar',
        'return_url': url,
    }

    return render(request, "comercial/pedido_add.html", context)


@login_required
def PedidoApagarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    pedido = get_object_or_404(Pedido, pk=pk)

    if pedido.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:pedido_listar_view')

    if request.method == 'POST':
        pedido.delete()
        return HttpResponseRedirect(url)
    
    form = PedidoForm(instance=pedido)
   
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    pedido_marcas = []

    if pedido.marcas:
        pedido_marcas = list(map(int, pedido.marcas.split(',')))

    context = {
        'form': form,
        'acao': 'apagar',
        'marcas': marcas,
        'pedido_marcas': pedido_marcas,
        'pretitle': 'Apagar',
        'return_url': url,
    }

    return render(request, "comercial/pedido_add.html", context)


@login_required
def PedidoVisualizarView(request, pk):

    pedido = get_object_or_404(Pedido, pk=pk)

    if pedido.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:pedido_listar_view')

    form = PedidoForm(instance=pedido, request=request)
   
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    pedido_marcas = []

    if pedido.marcas:
        pedido_marcas = list(map(int, pedido.marcas.split(',')))

    context = {
        'form': form,
        'acao': 'visualizar',
        'marcas': marcas,
        'pedido_marcas': pedido_marcas,
        'pretitle': 'Visualizar',
        'return_url': url,
    }

    return render(request, "comercial/pedido_add.html", context)


def PedidoListar(request, queryset, title):

    context = {
        'queryset': queryset,
        'action_search': reverse_lazy('comercial:pedido_pesquisar_view'),
        'pretitle': title,
    }
    
    if request.user.has_perm_cadastro_editar:
        context['add_url'] = reverse_lazy('comercial:pedido_adicionar_view')

    return render(request, 'comercial/pedido_listar.html', context)


@login_required
def PedidoListarView(request):
    #today = date.today()
    queryset = Pedido.objects.filter(
        credenciado=request.user.credenciado.pk,
        #cadastro__year__gte=today.year,
        #cadastro__month__gte=today.month
    ).order_by('-cadastro')[:100]
    return PedidoListar(request, queryset, 'Recentes')
    

@login_required
def PedidoPesquisarView(request):

    if request.method != 'GET' or not request.GET.get('q'):
        return HttpResponseRedirect(reverse_lazy('comercial:pedido_listar_view'))

    search = request.GET.get('q')
    search = search.strip()

    queryset = Pedido.objects.filter(credenciado=request.user.credenciado.pk)

    if len(search) == 18 and (search[2]+search[6]+search[10]+search[15]) == '../-':  # CNPJ
        queryset = queryset.filter(cliente__cnpj=search)

    elif len(search) == 14 and search.isnumeric():  # CNPJ
        search = search[0:2]+'.'+search[2:5]+'.'+search[5:8]+'/'+search[8:12]+'-'+search[12:]
        queryset = queryset.filter(cliente__cnpj=search)

    elif search.isnumeric():
        queryset = queryset.filter(pk=search)

    elif '@' in search:
        queryset = queryset.filter(cliente__email=search.lower())

    else:
        search = search.upper()
        if '*' in search:
            search = clear_text(search.replace('*', ''))
            queryset = queryset.filter(cliente__nome__contains=search)
        else:
            search = clear_text(search)
            queryset = queryset.filter(cliente__nome__startswith=search)

    return PedidoListar(request, queryset, 'Encontrados')


@login_required
def PedidoProcurarView(request):

    pedidos = []

    if request.method != 'GET':
        content = simplejson.dumps(pedidos)
        return HttpResponse(content, content_type='application/json')

    if request.GET.get('q'):
        search = request.GET.get('q').upper()

    queryset = pedido.objects.filter(credenciado=request.user.credenciado.pk)

    if request.GET.get('pk'):
        queryset = queryset.filter(pk=request.GET.get('pk'))
        
    elif len(search) == 18 and (search[2]+search[6]+search[10]+search[15]) == '../-':  # CNPJ
        queryset = queryset.filter(cnpj=search)

    elif len(search) == 14 and search.isnumeric():  # CNPJ
        search = search[0:2]+'.'+search[2:5]+'.'+search[5:8]+'/'+search[8:12]+'-'+search[12:]
        queryset = queryset.filter(cnpj=search)
    else:
        if '*' in search:
            search = clear_text(search.replace('*', ''))
            queryset = queryset.filter(nome__contains=search)
        else:
            search = clear_text(search)
            queryset = queryset.filter(nome__startswith=search)

    for pedido in queryset.all():
        pedidos.append({
                    'pk': pedido.pk, 
                    'nome': pedido.nome,
                })

    content = simplejson.dumps(pedidos)
    
    return HttpResponse(content, content_type='application/json')


@login_required
def PedidoProcurarNomeView(request):

    pedidos = []

    if request.method != 'GET':
        content = simplejson.dumps(pedidos)
        return HttpResponse(content, content_type='application/json')

    queryset = pedido.objects.filter(credenciado=request.user.credenciado.pk)

    search = clear_text(request.GET.get('q').upper())
    queryset = queryset.filter(nome=search)

    for pedido in queryset.all():
        pedidos.append({
                    'pk': pedido.pk, 
                    'nome': pedido.nome
                })

    content = simplejson.dumps(pedidos)

    return HttpResponse(content, content_type='application/json')
