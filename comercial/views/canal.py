from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from comercial.models import Canal
from comercial.forms import CanalForm


@login_required
def CanalAdicionarView(request):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:canal_listar_view')

    if request.method == 'POST':
        form = CanalForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = CanalForm(request=request)
    
    context = {
        'form': form,
        'acao': 'adicionar',
        'pretitle': 'Adicionar',
        'return_url': url,
    }

    return render(request, "comercial/canal_add.html", context)


@login_required
def CanalEditarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:canal_listar_view')

    canal = get_object_or_404(Canal, pk=pk)

    if canal.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = CanalForm(request.POST, instance=canal, request=request)
        if form.is_valid():
            canal.save()
            return HttpResponseRedirect(url)
    else:
        form = CanalForm(instance=canal, request=request)
   
    context = {
        'form': form,
        'acao': 'alterar',
        'pretitle': 'Alterar',
        'return_url': url,
    }

    return render(request, "comercial/canal_add.html", context)


@login_required
def CanalApagarView(request, pk):

    canal = get_object_or_404(Canal, pk=pk)

    if canal.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:canal_listar_view')

    if request.method == 'POST':
        canal.delete()
        return HttpResponseRedirect(url)
    
    form = CanalForm(instance=canal)
   
    context = {
        'form': form,
        'acao': 'apagar',
        'pretitle': 'Apagar',
        'return_url': url,
    }

    return render(request, "comercial/canal_add.html", context)


@login_required
def CanalVisualizarView(request, pk):

    canal = get_object_or_404(Canal, pk=pk)

    if canal.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    form = CanalForm(instance=canal, request=request)
   
    context = {
        'form': form,
        'acao': 'visualizar',
        'pretitle': 'Visualizar',
        'return_url': reverse_lazy('comercial:canal_listar_view'),
    }

    return render(request, "comercial/canal_add.html", context)


@login_required
def CanalListarView(request):
    
    queryset = Canal.objects.filter(credenciado=request.user.credenciado.pk)

    context = {
        'queryset': queryset,
        'action_filter': '...',        
        'pretitle': 'Todos',
    }
    
    context['add_url'] = reverse_lazy('comercial:canal_adicionar_view')

    return render(request, 'comercial/canal_listar.html', context)
