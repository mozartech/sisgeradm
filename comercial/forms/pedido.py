from django import forms

from comercial.models import Pedido


class PedidoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', 0)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Pedido
        fields = '__all__'

    def save(self, commit=True):
        
        instance = super().save(commit=False)
        instance.credenciado = self.request.user.credenciado.pk

        if commit:
            instance.save()

        return instance