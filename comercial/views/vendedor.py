from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from comercial.models import Vendedor
from comercial.forms import VendedorForm


@login_required
def VendedorAdicionarView(request):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:vendedor_listar_view')

    if request.method == 'POST':
        form = VendedorForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = VendedorForm(request=request)
    
    context = {
        'form': form,
        'acao': 'adicionar',
        'pretitle': 'Adicionar',
        'return_url': url,
    }

    return render(request, "comercial/vendedor_add.html", context)


@login_required
def VendedorEditarView(request, pk):

    if not request.user.has_perm_cadastro_editar:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:vendedor_listar_view')

    vendedor = get_object_or_404(Vendedor, pk=pk)

    if vendedor.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = VendedorForm(request.POST, instance=vendedor, request=request)
        if form.is_valid():
            vendedor.save()
            return HttpResponseRedirect(url)
    else:
        form = VendedorForm(instance=vendedor, request=request)
   
    context = {
        'form': form,
        'acao': 'alterar',
        'pretitle': 'Alterar',
        'return_url': url,
    }

    return render(request, "comercial/vendedor_add.html", context)


@login_required
def VendedorApagarView(request, pk):

    vendedor = get_object_or_404(Vendedor, pk=pk)

    if vendedor.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('comercial:vendedor_listar_view')

    if request.method == 'POST':
        vendedor.delete()
        return HttpResponseRedirect(url)
    
    form = VendedorForm(instance=vendedor)
   
    context = {
        'form': form,
        'acao': 'apagar',
        'pretitle': 'Apagar',
        'return_url': url,
    }

    return render(request, "comercial/vendedor_add.html", context)


@login_required
def VendedorVisualizarView(request, pk):

    vendedor = get_object_or_404(Vendedor, pk=pk)

    if vendedor.credenciado != request.user.credenciado.pk:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    form = VendedorForm(instance=vendedor, request=request)
   
    context = {
        'form': form,
        'acao': 'visualizar',
        'pretitle': 'Visualizar',
        'return_url': reverse_lazy('comercial:vendedor_listar_view'),
    }

    return render(request, "comercial/vendedor_add.html", context)


@login_required
def VendedorListarView(request):
    
    queryset = Vendedor.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    context = {
        'queryset': queryset,
        'action_filter': '...',
        'pretitle': 'Todos',
    }
    
    context['add_url'] = reverse_lazy('comercial:vendedor_adicionar_view')

    return render(request, 'comercial/vendedor_listar.html', context)
