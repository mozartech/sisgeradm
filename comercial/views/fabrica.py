import simplejson

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from comercial.models import Fabrica, Marca
from comercial.forms import FabricaForm
from base.utils import clear_text


@login_required
def FabricaAdicionarView(request):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:fabrica_listar_view')

    if request.method == 'POST':
        form = FabricaForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = FabricaForm(request=request)
    
    bairros = Fabrica.objects.filter(credenciado=request.user.credenciado.pk).order_by('endereco_bairro').distinct('endereco_bairro')
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    context = {
        'form': form,
        'acao': 'adicionar',
        'bairros': bairros,
        'marcas': marcas,
        'fabrica_marcas': [],
        'pretitle': 'Adicionar',
        'return_url': url,
    }

    return render(request, "comercial/fabrica_add.html", context)


@login_required
def FabricaEditarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:fabrica_listar_view')

    fabrica = get_object_or_404(Fabrica, pk=pk)

    if fabrica.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = FabricaForm(request.POST, instance=fabrica, request=request, id=pk)
        if form.is_valid():
            fabrica.save()
            return HttpResponseRedirect(url)
    else:
        form = FabricaForm(instance=fabrica, request=request, id=pk)
   
    bairros = Fabrica.objects.filter(
                    credenciado=request.user.credenciado.pk
            ).order_by('endereco_bairro').distinct('endereco_bairro')
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    fabrica_marcas = []
    if fabrica.marcas:
        fabrica_marcas = list(map(int, fabrica.marcas.split(',')))

    context = {
        'form': form,
        'acao': 'alterar',
        'bairros': bairros,
        'marcas': marcas,
        'fabrica_marcas': fabrica_marcas,
        'pretitle': 'Alterar',
        'return_url': url,
    }

    return render(request, "comercial/fabrica_add.html", context)


@login_required
def FabricaApagarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    fabrica = get_object_or_404(Fabrica, pk=pk)

    if fabrica.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:fabrica_listar_view')

    if request.method == 'POST':
        fabrica.delete()
        return HttpResponseRedirect(url)
    
    form = FabricaForm(instance=fabrica)
   
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    fabrica_marcas = []

    if fabrica.marcas:
        fabrica_marcas = list(map(int, fabrica.marcas.split(',')))

    context = {
        'form': form,
        'marcas': marcas,        
        'fabrica_marcas': fabrica_marcas,
        'acao': 'apagar',
        'pretitle': 'Apagar',
        'return_url': url,
    }

    return render(request, "comercial/fabrica_add.html", context)


@login_required
def FabricaVisualizarView(request, pk):

    fabrica = get_object_or_404(Fabrica, pk=pk)

    if fabrica.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    form = FabricaForm(instance=fabrica, request=request)
   
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    fabrica_marcas = []
    
    if fabrica.marcas:
        fabrica_marcas = list(map(int, fabrica.marcas.split(',')))

    context = {
        'form': form,
         'marcas': marcas,
         'fabrica_marcas': fabrica_marcas,
        'acao': 'visualizar',
        'pretitle': 'Visualizar',
        'return_url': reverse_lazy('comercial:fabrica_listar_view'),
    }

    return render(request, "comercial/fabrica_add.html", context)


def FabricaListar(request, queryset, title):

    context = {
        'queryset': queryset,
        'action_search': reverse_lazy('comercial:fabrica_pesquisar_view'),
        'pretitle': title,
    }
    
    if request.user.has_perm_cadastro_editar:
        context['add_url'] = reverse_lazy('comercial:fabrica_adicionar_view')

    return render(request, 'comercial/fabrica_listar.html', context)


@login_required
def FabricaListarView(request):
    queryset = Fabrica.objects.filter(credenciado=request.user.credenciado.pk).order_by("-cadastro")[:10]
    return FabricaListar(request, queryset, 'Recentes')
    

def is_telefone(codigo):

    lista = codigo.split('-')

    return len(lista) == 2 and lista[0].isnumeric() and lista[1].isnumeric() and \
           len(lista[0]) in [4, 5] and len(lista[1]) == 4
    
    
@login_required
def FabricaPesquisarView(request):

    if request.method != 'GET' or not request.GET.get('q'):
        return HttpResponseRedirect(reverse_lazy('comercial:fabrica_listar_view'))

    search = request.GET.get('q')
    search = search.strip()

    queryset = Fabrica.objects.filter(credenciado=request.user.credenciado.pk)

    if len(search) == 18 and (search[2]+search[6]+search[10]+search[15]) == '../-':  # CNPJ
        queryset = queryset.filter(cnpj=search)

    elif len(search) == 14 and search.isnumeric():  # CNPJ
        search = search[0:2]+'.'+search[2:5]+'.'+search[5:8]+'/'+search[8:12]+'-'+search[12:]
        queryset = queryset.filter(cnpj=search)

    elif '@' in search:
        queryset = queryset.filter(email=search.lower())

    elif is_telefone(search):
        queryset = queryset.filter(telefone__contains=search)

    else:
        search = search.upper()
        if '*' in search:
            search = clear_text(search.replace('*', ''))
            queryset = queryset.filter(nome__contains=search)
        else:
            search = clear_text(search)
            queryset = queryset.filter(nome__startswith=search)

    return FabricaListar(request, queryset, 'Encontrados')


@login_required
def FabricaProcurarView(request):

    fabricas = []

    if request.method != 'GET':
        content = simplejson.dumps(fabricas)
        return HttpResponse(content, content_type='application/json')

    if request.GET.get('q'):
        search = request.GET.get('q').upper()

    queryset = Fabrica.objects.filter(credenciado=request.user.credenciado.pk)

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

    for fabrica in queryset.all():
        fabricas.append({
                    'pk': fabrica.pk, 
                    'nome': fabrica.nome,
                })

    content = simplejson.dumps(fabricas)
    
    return HttpResponse(content, content_type='application/json')


@login_required
def FabricaProcurarNomeView(request):

    fabricas = []

    if request.method != 'GET':
        content = simplejson.dumps(fabricas)
        return HttpResponse(content, content_type='application/json')

    queryset = Fabrica.objects.filter(credenciado=request.user.credenciado.pk)

    search = clear_text(request.GET.get('q').upper())
    queryset = queryset.filter(nome=search)

    for fabrica in queryset.all():
        fabricas.append({
                    'pk': fabrica.pk, 
                    'nome': fabrica.nome
                })

    content = simplejson.dumps(fabricas)

    return HttpResponse(content, content_type='application/json')
