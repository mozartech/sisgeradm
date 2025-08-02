from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from comercial.models import Status
from comercial.forms import StatusForm


@login_required
def StatusAdicionarView(request):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:status_listar_view')

    if request.method == 'POST':
        form = StatusForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = StatusForm(request=request)
    
    context = {
        'form': form,
        'acao': 'adicionar',
        'pretitle': 'Adicionar',
        'return_url': url,
    }

    return render(request, "comercial/status_add.html", context)


@login_required
def StatusEditarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:status_listar_view')

    status = get_object_or_404(Status, pk=pk)

    if status.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status, request=request)
        if form.is_valid():
            status.save()
            return HttpResponseRedirect(url)
    else:
        form = StatusForm(instance=status, request=request)
   
    context = {
        'form': form,
        'acao': 'alterar',
        'pretitle': 'Alterar',
        'return_url': url,
    }

    return render(request, "comercial/status_add.html", context)


@login_required
def StatusApagarView(request, pk):

    status = get_object_or_404(Status, pk=pk)

    if status.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:status_listar_view')

    if request.method == 'POST':
        status.delete()
        return HttpResponseRedirect(url)
    
    form = StatusForm(instance=status)
   
    context = {
        'form': form,
        'acao': 'apagar',
        'pretitle': 'Apagar',
        'return_url': url,
    }

    return render(request, "comercial/status_add.html", context)


@login_required
def StatusVisualizarView(request, pk):

    status = get_object_or_404(Status, pk=pk)

    if status.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    form = StatusForm(instance=status, request=request)
   
    context = {
        'form': form,
        'acao': 'visualizar',
        'pretitle': 'Visualizar',
        'return_url': reverse_lazy('comercial:status_listar_view'),
    }

    return render(request, "comercial/status_add.html", context)


@login_required
def StatusListarView(request):
    
    queryset = Status.objects.filter(credenciado=request.user.credenciado.pk)

    context = {
        'queryset': queryset,
        'action_filter': '...',        
        'pretitle': 'Todos',
    }
    
    context['add_url'] = reverse_lazy('comercial:status_adicionar_view')

    return render(request, 'comercial/status_listar.html', context)
