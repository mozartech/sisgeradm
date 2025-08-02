from django import forms

from comercial.models import Fabrica


class FabricaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', 0)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Fabrica
        fields = '__all__'
        widgets = {
            'endereco_cidade': forms.Select(),
            'ativo': forms.CheckboxInput()
        }

    def clean(self):

        cleaned_data = super().clean()

        cnpj = cleaned_data.get('cnpj')

        qs = Fabrica.objects.filter(credenciado=self.request.user.credenciado.pk,
                                    cnpj=cnpj).exclude(pk=self.id)

        if qs.count() > 0:
            self.add_error('cpf', 'Fabrica duplicada, mesmo CNPJ. Gravação não efetuada. Verifique')

    def save(self, commit=True):
        
        instance = super().save(commit=False)
        instance.credenciado = self.request.user.credenciado.pk

        if commit:
            instance.save()

        return instance