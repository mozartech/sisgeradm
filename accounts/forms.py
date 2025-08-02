from django import forms
from django.core.exceptions import ValidationError

from .models import USER_COMUM, MyUser, Credenciado
from .models import USER_ADMINISTRADOR, USER_PERFIL, USER_SUPER


class CredenciadoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Credenciado
        fields = "__all__"
        widgets = {
            'endereco_cidade': forms.Select()
        }


class UsuarioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'telefone', 'is_active')

    def clean_email(self):
        data = self.cleaned_data['email']
        if not data:
            raise ValidationError('O e-mail é obrigatório')
        return data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.credenciado = self.request.user.credenciado
        instance.is_staff = False  # sem acesso ao admin
        instance.is_superuser = True
        instance.perfil = USER_COMUM
        if not instance.password:
            instance.set_password(instance.email)
        if commit:
            instance.save()
        return instance


class UsuarioPerfil(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = MyUser
        fields = (
            'first_name', 'last_name', 'email', 'telefone',
            'tema', 'layout', 'fluid', 'nav_sticky', 'nav_color'
        )

    def clean_email(self):
        return self.instance.email
    
    def clean_perfil(self):
        return self.instance.perfil


class AdministradorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'telefone', 'is_active')

    def clean_email(self):
        data = self.cleaned_data['email']
        if not data:
            raise ValidationError('O e-mail é obrigatório')
        return data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_staff = False  # sem acesso ao admin
        instance.perfil = USER_ADMINISTRADOR
        instance.is_superuser = True
        if not instance.password:
            instance.set_password(instance.email)
        if commit:
            instance.save()
        return instance


class SuperUsuarioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['credenciado'].choices = []
        for credenciado in Credenciado.objects.all():
            self.fields['credenciado'].choices.append((credenciado.pk, credenciado.nome))

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'telefone', 'credenciado', 'is_active')

    def clean_email(self):
        data = self.cleaned_data['email']
        if not data:
            raise ValidationError('O e-mail é obrigatório')
        return data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_staff = False  # sem acesso ao admin
        instance.perfil = USER_SUPER
        instance.credenciado = self.request.user.credenciado
        instance.is_superuser = True
        if not instance.password:
            instance.set_password(instance.email)
        if commit:
            instance.save()
        return instance