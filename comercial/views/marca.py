from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from comercial.models import Marca
from comercial.forms import MarcaForm


@login_required
def MarcaAdicionarView(request):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:marca_listar_view')

    if request.method == 'POST':
        form = MarcaForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = MarcaForm(request=request)
    
    context = {
        'form': form,
        'acao': 'adicionar',
        'pretitle': 'Adicionar',
        'return_url': url,
    }

    return render(request, "comercial/marca_add.html", context)


@login_required
def MarcaEditarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:marca_listar_view')

    marca = get_object_or_404(Marca, pk=pk)

    if marca.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca, request=request)
        if form.is_valid():
            marca.save()
            return HttpResponseRedirect(url)
    else:
        form = MarcaForm(instance=marca, request=request)
   
    context = {
        'form': form,
        'acao': 'alterar',
        'pretitle': 'Alterar',
        'return_url': url,
    }

    return render(request, "comercial/marca_add.html", context)


@login_required
def MarcaApagarView(request, pk):

    marca = get_object_or_404(Marca, pk=pk)

    if marca.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:marca_listar_view')

    if request.method == 'POST':
        marca.delete()
        return HttpResponseRedirect(url)
    
    form = MarcaForm(instance=marca)
   
    context = {
        'form': form,
        'acao': 'apagar',
        'pretitle': 'Apagar',
        'return_url': url,
    }

    return render(request, "comercial/marca_add.html", context)


@login_required
def MarcaVisualizarView(request, pk):

    marca = get_object_or_404(Marca, pk=pk)

    if marca.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    form = MarcaForm(instance=marca, request=request)
   
    context = {
        'form': form,
        'acao': 'visualizar',
        'pretitle': 'Visualizar',
        'return_url': reverse_lazy('comercial:marca_listar_view'),
    }

    return render(request, "comercial/marca_add.html", context)


@login_required
def MarcaListarView(request):
    
    queryset = Marca.objects.filter(credenciado=request.user.credenciado.pk)

    context = {
        'queryset': queryset,
        'action_filter': '...',        
        'pretitle': 'Todas',
    }
    
    context['add_url'] = reverse_lazy('comercial:marca_adicionar_view')

    return render(request, 'comercial/marca_listar.html', context)
