from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from comercial.models import Grupo
from comercial.forms import GrupoForm


@login_required
def GrupoAdicionarView(request):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:grupo_listar_view')

    if request.method == 'POST':
        form = GrupoForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = GrupoForm(request=request)
    
    context = {
        'form': form,
        'acao': 'adicionar',
        'pretitle': 'Adicionar',
        'return_url': url,
    }

    return render(request, "comercial/grupo_add.html", context)


@login_required
def GrupoEditarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:grupo_listar_view')

    grupo = get_object_or_404(Grupo, pk=pk)

    if grupo.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = GrupoForm(request.POST, instance=grupo, request=request)
        if form.is_valid():
            grupo.save()
            return HttpResponseRedirect(url)
    else:
        form = GrupoForm(instance=grupo, request=request)
   
    context = {
        'form': form,
        'acao': 'alterar',
        'pretitle': 'Alterar',
        'return_url': url,
    }

    return render(request, "comercial/grupo_add.html", context)


@login_required
def GrupoApagarView(request, pk):

    grupo = get_object_or_404(Grupo, pk=pk)

    if grupo.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:grupo_listar_view')

    if request.method == 'POST':
        grupo.delete()
        return HttpResponseRedirect(url)
    
    form = GrupoForm(instance=grupo)
   
    context = {
        'form': form,
        'acao': 'apagar',
        'pretitle': 'Apagar',
        'return_url': url,
    }

    return render(request, "comercial/grupo_add.html", context)


@login_required
def GrupoVisualizarView(request, pk):

    grupo = get_object_or_404(Grupo, pk=pk)

    if grupo.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    form = GrupoForm(instance=grupo, request=request)
   
    context = {
        'form': form,
        'acao': 'visualizar',
        'pretitle': 'Visualizar',
        'return_url': reverse_lazy('comercial:grupo_listar_view'),
    }

    return render(request, "comercial/grupo_add.html", context)


@login_required
def GrupoListarView(request):
    
    queryset = Grupo.objects.filter(credenciado=request.user.credenciado.pk)

    context = {
        'queryset': queryset,
        'action_filter': '...',        
        'pretitle': 'Todos',
    }
    
    context['add_url'] = reverse_lazy('comercial:grupo_adicionar_view')

    return render(request, 'comercial/grupo_listar.html', context)
