import re

from django import forms

from comercial.models import Cliente


class ClienteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', 0)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'endereco_cidade': forms.Select(),
            'ativo': forms.CheckboxInput()
        }

    def clean(self):

        cleaned_data = super().clean()

        pessoa = cleaned_data.get('pessoa')

        if pessoa == 'PF':
            chave = cleaned_data.get('cpf')
        else:
            chave = cleaned_data.get('cnpj')

        chave = ''.join(re.findall(r'\d+', chave))
        
        qs = Cliente.objects.filter(credenciado=self.request.user.credenciado.pk,
                                    chave=chave).exclude(pk=self.id)

        if qs.count() > 0:
            if pessoa == 'PF':
                self.add_error('cpf', 'Cliente duplicado, mesmo CPF. Gravação não efetuada. Verifique')
            else:
                self.add_error('cnpj', 'Cliente duplicado, mesmo CNPJ. Gravação não efetuada. Verifique')

    def save(self, commit=True):
        
        instance = super().save(commit=False)
        instance.usuario = self.request.user
        instance.credenciado = self.request.user.credenciado.pk

        if commit:
            instance.save()

        return instance