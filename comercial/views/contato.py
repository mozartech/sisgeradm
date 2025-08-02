from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from comercial.models import Contato
from comercial.forms import ContatoForm

from base.models import CONTATO_TIPO
from .utils import to_yyyymmdd

@login_required
def ContatoAdicionarView(request):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:contato_listar_view')

    if request.method == 'POST':
        form = ContatoForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = ContatoForm(request=request)
    
    context = {
        'form': form,
        'acao': 'adicionar',
        'pretitle': 'Adicionar',
        'return_url': url,
        'funcoes': CONTATO_TIPO,
        'contato_funcoes': []
    }

    return render(request, "comercial/contato_add.html", context)


@login_required
def ContatoEditarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:contato_listar_view')

    contato = get_object_or_404(Contato, pk=pk)

    if contato.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = ContatoForm(request.POST, instance=contato, request=request)
        if form.is_valid():
            contato.save()
            return HttpResponseRedirect(url)
    else:
        form = ContatoForm(instance=contato, request=request)

    contato_funcoes = []

    if contato.funcao:
        contato_funcoes = contato.funcao.split(',')

    context = {
        'form': form,
        'acao': 'alterar',
        'pretitle': 'Alterar',
        'return_url': url,
        'contato_funcoes': contato_funcoes,
        'funcoes': CONTATO_TIPO
    }

    return render(request, "comercial/contato_add.html", context)


@login_required
def ContatoApagarView(request, pk):

    contato = get_object_or_404(Contato, pk=pk)

    if contato.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:contato_listar_view')

    if request.method == 'POST':
        contato.delete()
        return HttpResponseRedirect(url)
    
    form = ContatoForm(instance=contato)
   
    contato_funcoes = []

    if contato.funcao:
        contato_funcoes = contato.funcao.split(',')

    context = {
        'form': form,
        'acao': 'apagar',
        'pretitle': 'Apagar',
        'return_url': url,
        'contato_funcoes': contato_funcoes,
        'funcoes': CONTATO_TIPO                
    }

    return render(request, "comercial/contato_add.html", context)


@login_required
def ContatoVisualizarView(request, pk):

    contato = get_object_or_404(Contato, pk=pk)

    if contato.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    form = ContatoForm(instance=contato, request=request)
   
    contato_funcoes = []

    if contato.funcao:
        contato_funcoes = contato.funcao.split(',')

    context = {
        'form': form,
        'acao': 'visualizar',
        'pretitle': 'Visualizar',
        'return_url': reverse_lazy('comercial:contato_listar_view'),
        'funcoes': CONTATO_TIPO,
        'contato_funcoes': contato_funcoes,
    }

    return render(request, "comercial/contato_add.html", context)


@login_required
def ContatoListarView(request):
    
    queryset = Contato.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    context = {
        'queryset': queryset,
        'action_filter': '...',
        'pretitle': 'Todos',
    }
    
    context['add_url'] = reverse_lazy('comercial:contato_adicionar_view')

    return render(request, 'comercial/contato_listar.html', context)


@login_required
def ContatoAdicionarJson(request):

    resposta = {}

    try:
        contato = Contato.objects.get(credenciado=request.user.credenciado.pk,
                                      nome=request.GET['nome'])
        resposta = {'resposta': 'Já existe contato com esse nome'}
    except Contato.DoesNotExist:
        nascimento = request.GET['nascimento']
        if nascimento:
            nascimento = to_yyyymmdd(nascimento)
        else:
            nascimento = None
        contato = Contato()
        contato.credenciado = request.user.credenciado.pk
        contato.nome = request.GET['nome']
        contato.funcao = request.GET['funcao']
        contato.nascimento = nascimento
        contato.email = request.GET['email']
        contato.telefone1 = request.GET['telefone1']
        contato.telefone2 = request.GET['telefone2']
        contato.empresa = request.GET['empresa']
        contato.observacao = request.GET['observacao']
        contato.save()
        resposta = {'resposta': '1',
                    'id': contato.pk,
                    'nome': contato.nome}

    return JsonResponse(resposta)
   