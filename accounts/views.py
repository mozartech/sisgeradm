from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import (
    MyUser,
    USER_PROPRIETARIO, USER_ADMINISTRADOR, USER_SUPER, USER_COMUM
)

from base.models import Credenciado

from .forms import (
    SuperUsuarioForm, UsuarioForm,
    UsuarioPerfil, CredenciadoForm, AdministradorForm
)


@login_required
def CredenciadoListarView(request):

    if request.user.perfil != USER_ADMINISTRADOR:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    queryset = Credenciado.objects.all()

    context = {
        'queryset': queryset,
        'action_filter': '...',
        'add_url': reverse_lazy('accounts:credenciado_adicionar_view'),
        'pretitle': 'Todos'
    }

    return render(request, 'usuario/credenciado_listar.html', context)

@login_required
def CredenciadoAdicionarView(request):

    if request.user.perfil != USER_ADMINISTRADOR:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('accounts:credenciado_listar_view')

    if request.method == 'POST':
        form = CredenciadoForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = CredenciadoForm(request=request)

    context = {
        'form': form,
        'acao': 'adicionar',
        'pretitle': 'Adicionar',
        'return_url': url,
    }

    return render(request, 'usuario/credenciado_add.html', context)

@login_required
def CredenciadoEditarView(request, pk):

    if request.user.perfil != USER_ADMINISTRADOR:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    object = get_object_or_404(Credenciado, pk=pk)

    url = reverse_lazy('accounts:credenciado_listar_view')

    if request.method == 'POST':
        form = CredenciadoForm(request.POST, instance=object, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = CredenciadoForm(instance=object, request=request)

    context = {
        'form': form,
        'acao': 'alterar',
        'pretitle': 'Alterar',
        'return_url': url,
    }

    return render(request, 'usuario/credenciado_add.html', context)

@login_required
def CredenciadoVerView(request, pk):

    if request.user.perfil != USER_ADMINISTRADOR:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    object = get_object_or_404(Credenciado, pk=pk)

    url = reverse_lazy('accounts:credenciado_listar_view')

    form = CredenciadoForm(instance=object, request=request)

    context = {
        'form': form,
        'acao': 'visualizar',
        'pretitle': 'Visualizar',
        'return_url': url,
    }

    return render(request, 'usuario/credenciado_add.html', context)

@login_required
def CredenciadoApagarView(request, pk):

    if request.user.perfil != USER_ADMINISTRADOR:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    object = get_object_or_404(Credenciado, pk=pk)

    url = reverse_lazy('accounts:credenciado_listar_view')

    if request.method == 'POST':
        object.delete()
        return HttpResponseRedirect(url)
    else:
        form = CredenciadoForm(instance=object, request=request)

    context = {
        'form': form,
        'acao': 'apagar',
        'pretitle': 'Apagar',
        'return_url': url,
    }

    return render(request, 'usuario/credenciado_add.html', context)

@login_required
def CredenciadoPerfilView(request):

    credenciado = get_object_or_404(Credenciado, pk=request.user.credenciado.pk)

    if request.method == 'POST':
        form = CredenciadoForm(request.POST, instance=credenciado, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('base:index'))
    else:
        form = CredenciadoForm(instance=credenciado, request=request)

    context = {
        'form': form,
        'acao': 'alterar',
        'pretitle': 'Perfil',
        'return_url': reverse_lazy('base:index'),
    }

    return render(request, "usuario/credenciado_perfil.html", context)


@login_required
def CredenciadoAtivarView(request, pk):

    url = reverse_lazy('accounts:credenciado_listar_view')

    credenciado = get_object_or_404(Credenciado, pk=pk)

    if request.method == 'POST':
        
        request.user.credenciado = credenciado
        request.user.save()
        
        return HttpResponseRedirect(url)

    else:
        form = CredenciadoForm(instance=credenciado, request=request)

    context = {
        'form': form,
        'acao': 'ativar',
        'pretitle': 'Ativar',
        'return_url': url,
    }

    return render(request, "usuario/credenciado_add.html", context)


@login_required
def UsuarioListarView(request):

    if not request.user.has_perm_user:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    queryset = MyUser.objects.filter(credenciado=request.user.credenciado,
                                     perfil=USER_COMUM).exclude(pk=request.user.pk)

    url = reverse_lazy('accounts:usuario_listar_view')

    context = {
        'queryset': queryset,
        'action_filter': '...',
        'return_url': url,
        'pretitle': 'Todos',
    }

    if request.user.perfil in [USER_ADMINISTRADOR, USER_SUPER]:
        context['add_url'] = reverse_lazy('accounts:usuario_adicionar_view')

    return render(request, "usuario/usuario_list.html", context)


@login_required
def UsuarioVisualizarView(request, pk):

    if not request.user.has_perm_user:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('accounts:usuario_listar_view')
    usuario = get_object_or_404(MyUser, pk=pk)

    if usuario.credenciado != request.user.credenciado:
        return HttpResponseRedirect(url)

    if usuario.perfil in [USER_PROPRIETARIO, USER_ADMINISTRADOR]:
        return HttpResponseRedirect(url)

    form = UsuarioForm(instance=usuario, request=request)

    context = {
        'form': form,
        'acao': 'visualizar',
        'pretitle': 'Visualizar',
        'return_url': url,
    }

    return render(request, "usuario/usuario_add.html", context)

@login_required
def UsuarioAdicionarView(request):

    if not request.user.perfil in [USER_SUPER, USER_ADMINISTRADOR]:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('accounts:usuario_listar_view')
    
    if request.method == 'POST':
        
        form = UsuarioForm(request.POST, request=request)

        if form.is_valid():
            
            data_email = form.cleaned_data["email"]

            qs = MyUser.objects.filter(credenciado=request.user.credenciado, email=data_email)

            if qs.count() > 0:
                form.add_error("email", "Um usuário já possui esse e-mail")
            else:
                form.save()
                return HttpResponseRedirect(url)

    else:
        form = UsuarioForm(request=request)

    context = {
        'form': form,
        'acao': 'adicionar',
        'return_url': url,
        'pretitle': 'Adicionar',
    }

    return render(request, "usuario/usuario_add.html", context)

@login_required
def UsuarioEditarView(request, pk):

    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    if not request.user.perfil in [USER_SUPER, USER_ADMINISTRADOR]:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    usuario = get_object_or_404(MyUser, pk=pk)
    url = reverse_lazy('accounts:usuario_listar_view')

    if usuario.credenciado != request.user.credenciado:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario, request=request)
        if form.is_valid():
            data_email = form.cleaned_data["email"]
            qs = MyUser.objects.filter(credenciado=request.user.credenciado, email=data_email)
            qs = qs.exclude(pk=usuario.id)
            if qs.count() > 0:
                form.add_error("email", "Um outro usuário já possui esse e-mail")
            else:
                form.save()
                return HttpResponseRedirect(url)
    else:
        form = UsuarioForm(instance=usuario, request=request)

    context = {
        'form': form,
        'acao': 'alterar',
        'pretitle': 'Alterar',
        'return_url': url,
    }

    return render(request, "usuario/usuario_add.html", context)

@login_required
def UsuarioApagarView(request, pk):

    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    if not request.user.perfil in [USER_ADMINISTRADOR, USER_SUPER]:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    usuario = get_object_or_404(MyUser, pk=pk)
    url = reverse_lazy('accounts:usuario_listar_view')

    if usuario.credenciado != request.user.credenciado:
        return HttpResponseRedirect(url)

    if usuario.perfil in [USER_PROPRIETARIO, USER_ADMINISTRADOR, USER_SUPER]:
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        usuario.delete()
        return HttpResponseRedirect(url)

    form = UsuarioForm(instance=usuario, request=request)
   
    context = {
        'form': form,
        'acao': 'apagar',
        'pretitle': 'Apagar',
        'return_url': url,
    }

    return render(request, "usuario/usuario_add.html", context)

@login_required
def UsuarioPerfilView(request):

    usuario = get_object_or_404(MyUser, pk=request.user.id)
    url = reverse_lazy('base:index')

    if request.method == 'POST':
        form = UsuarioPerfil(request.POST, instance=usuario, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(url)
    else:
        form = UsuarioPerfil(instance=usuario, request=request)

    context = {
        'form': form,
        'acao': 'alterar',
        'pretitle': 'Perfil',
        'return_url': url
    }

    return render(request, "usuario/usuario_perfil.html", context)

# view de usuários administradores

@login_required
def AdministradorListarView(request):

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    if request.user.perfil != USER_PROPRIETARIO:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    queryset = MyUser.objects.filter(perfil=USER_ADMINISTRADOR).order_by("first_name")

    context = {
        'queryset': queryset,
        'add_url': reverse_lazy('accounts:administrador_adicionar_view'),
        'action_filter': '...',
        'pretitle': 'Todos'
    }

    return render(request, "usuario/administrador_lista.html", context)


@login_required
def AdministradorAdicionarView(request):

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    if request.user.perfil != USER_PROPRIETARIO:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy("accounts:administrador_listar_view")
    
    if request.method == "POST":
        form = AdministradorForm(request.POST, request=request)
        if form.is_valid():
            data_email = form.cleaned_data["email"]
            qs = MyUser.objects.filter(email=data_email, is_active=True)
            if qs.count() > 0:
                form.add_error("email", "Um usuário já possui esse e-mail")
            else:
                form.save()
                return HttpResponseRedirect(url)
    else:
        form = AdministradorForm(request=request)

    context = {
        "form": form,
        "acao": "adicionar",
        "return_url": url,
        "pretitle": "Adicionar"
    }

    return render(request, "usuario/administrador_add.html", context)

@login_required
def AdministradorVisualizarView(request, pk):

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    if request.user.perfil != USER_PROPRIETARIO:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    usuario = get_object_or_404(MyUser, pk=pk)
    url = reverse_lazy('accounts:administrador_listar_view')

    form = AdministradorForm(instance=usuario, request=request)

    context = {
        'form': form,
        'acao': 'visualizar',
        'return_url': url,
        'pretitle': 'Visualizar'
    }

    return render(request, "usuario/administrador_add.html", context)

@login_required
def AdministradorEditarView(request, pk):

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    if request.user.perfil != USER_PROPRIETARIO:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    usuario = get_object_or_404(MyUser, pk=pk)
    url = reverse_lazy('accounts:administrador_listar_view')

    if request.method == 'POST':
        form = AdministradorForm(request.POST, instance=usuario, request=request)
        if form.is_valid():
            data_email = form.cleaned_data["email"]
            qs = MyUser.objects.filter(email=data_email, is_active=True)
            qs = qs.exclude(pk=usuario.id)
            if qs.count() > 0:
                form.add_error("email", "Um outro administrador já possui esse e-mail")
            else:
                form.save()
                return HttpResponseRedirect(url)
    else:
        form = AdministradorForm(instance=usuario, request=request)

    context = {
        'form': form,
        'acao': 'alterar',
        'return_url': url,
        'pretitle': 'Alterar'
    }

    return render(request, "usuario/administrador_add.html", context)

@login_required
def AdministradorApagarView(request, pk):

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse_lazy('base:index'))
    
    if request.user.perfil != USER_PROPRIETARIO:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    usuario = get_object_or_404(MyUser, pk=pk)
    url = reverse_lazy('accounts:administrador_listar_view')

    if request.method == 'POST':
        usuario.delete()
        return HttpResponseRedirect(url)

    form = AdministradorForm(instance=usuario, request=request)

    context = {
        'form': form,
        'acao': 'apagar',
        'return_url': url,
        'pretitle': 'Apagar'
    }

    return render(request, "usuario/administrador_add.html", context)

# view de usuários superusuarios

@login_required
def SuperUsuarioListarView(request):

    if request.user.perfil != USER_ADMINISTRADOR:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    queryset = MyUser.objects.filter(credenciado=request.user.credenciado, perfil=USER_SUPER)

    context = {
        'queryset': queryset,
        'add_url': reverse_lazy('accounts:superusuario_adicionar_view'),
        'action_filter': '...',
        'pretitle': 'Todos'
    }

    return render(request, 'usuario/superusuario_listar.html', context)

@login_required
def SuperUsuarioAdicionarView(request):

    if request.user.perfil != USER_ADMINISTRADOR:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('accounts:superusuario_listar_view')
    
    if request.method == 'POST':
        form = SuperUsuarioForm(request.POST, request=request)
        if form.is_valid():
            data_email = form.cleaned_data['email']
            qs = MyUser.objects.filter(credenciado=request.user.credenciado, email=data_email)
            if qs.count() > 0:
                form.add_error('email', 'Um usuário já possui esse e-mail')
            else:
                form.save()
                return HttpResponseRedirect(url)
    else:
        form = SuperUsuarioForm(request=request)

    context = {
        'form': form,
        'acao': 'adicionar',
        'return_url': url,
        'pretitle': 'Adicionar'
    }

    return render(request, 'usuario/superusuario_add.html', context)


@login_required
def SuperUsuarioVisualizarView(request, pk):

    if request.user.perfil != USER_ADMINISTRADOR:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    usuario = get_object_or_404(MyUser, pk=pk)

    if usuario.perfil != USER_SUPER or usuario.credenciado != request.user.credenciado:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('accounts:superusuario_listar_view')
    form = SuperUsuarioForm(instance=usuario, request=request)

    context = {
        'form': form,
        'acao': 'visualizar',
        'return_url': url,
        'pretitle': 'Visualizar'
    }

    return render(request, 'usuario/superusuario_add.html', context)


@login_required
def SuperUsuarioEditarView(request, pk):

    if request.user.perfil != USER_ADMINISTRADOR:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    usuario = get_object_or_404(MyUser, pk=pk)

    if usuario.perfil != USER_SUPER or usuario.credenciado != request.user.credenciado:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    url = reverse_lazy('accounts:superusuario_listar_view')

    if request.method == 'POST':
        form = SuperUsuarioForm(request.POST, instance=usuario, request=request)
        if form.is_valid():
            data_email = form.cleaned_data["email"]
            qs = MyUser.objects.filter(credenciado=request.user.credenciado, email=data_email)
            qs = qs.exclude(pk=usuario.id)
            if qs.count() > 0:
                form.add_error('email', 'Um outro usuário já possui esse e-mail')
            else:
                form.save()
                return HttpResponseRedirect(url)
    else:
        form = SuperUsuarioForm(instance=usuario, request=request)

    context = {
        'form': form,
        'acao': 'alterar',
        'return_url': url,
        'pretitle': 'Alterar'
    }

    return render(request, 'usuario/superusuario_add.html', context)


@login_required
def SuperUsuarioApagarView(request, pk):

    if request.user.perfil != USER_ADMINISTRADOR:
        return HttpResponseRedirect(reverse_lazy('base:index'))

    usuario = get_object_or_404(MyUser, pk=pk)

    url = reverse_lazy('accounts:superusuario_listar_view')

    if request.method == 'POST':
        usuario.delete()
        return HttpResponseRedirect(url)

    form = SuperUsuarioForm(instance=usuario, request=request)

    context = {
        'form': form,
        'acao': 'apagar',
        'return_url': url,
        'pretitle': 'Apagar'
    }

    return render(request, 'usuario/superusuario_add.html', context)