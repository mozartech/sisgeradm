from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from comercial.models import Segmento
from comercial.forms import SegmentoForm


@login_required
def SegmentoAdicionarView(request):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:segmento_listar_view')

    if request.method == 'POST':
        form = SegmentoForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = SegmentoForm(request=request)
    
    context = {
        'form': form,
        'acao': 'adicionar',
        'pretitle': 'Adicionar',
        'return_url': url,
    }

    return render(request, "comercial/segmento_add.html", context)


@login_required
def SegmentoEditarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:segmento_listar_view')

    segmento = get_object_or_404(Segmento, pk=pk)

    if segmento.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = SegmentoForm(request.POST, instance=segmento, request=request)
        if form.is_valid():
            segmento.save()
            return HttpResponseRedirect(url)
    else:
        form = SegmentoForm(instance=segmento, request=request)
   
    context = {
        'form': form,
        'acao': 'alterar',
        'pretitle': 'Alterar',
        'return_url': url,
    }

    return render(request, "comercial/segmento_add.html", context)


@login_required
def SegmentoApagarView(request, pk):

    segmento = get_object_or_404(Segmento, pk=pk)

    if segmento.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:segmento_listar_view')

    if request.method == 'POST':
        segmento.delete()
        return HttpResponseRedirect(url)
    
    form = SegmentoForm(instance=segmento)
   
    context = {
        'form': form,
        'acao': 'apagar',
        'pretitle': 'Apagar',
        'return_url': url,
    }

    return render(request, "comercial/segmento_add.html", context)


@login_required
def SegmentoVisualizarView(request, pk):

    segmento = get_object_or_404(Segmento, pk=pk)

    if segmento.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    form = SegmentoForm(instance=segmento, request=request)
   
    context = {
        'form': form,
        'acao': 'visualizar',
        'pretitle': 'Visualizar',
        'return_url': reverse_lazy('comercial:segmento_listar_view'),
    }

    return render(request, "comercial/segmento_add.html", context)


@login_required
def SegmentoListarView(request):
    
    queryset = Segmento.objects.filter(credenciado=request.user.credenciado.pk)

    context = {
        'queryset': queryset,
        'action_filter': '...',        
        'pretitle': 'Todos',
    }
    
    context['add_url'] = reverse_lazy('comercial:segmento_adicionar_view')

    return render(request, 'comercial/segmento_listar.html', context)
