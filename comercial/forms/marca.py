from django import forms

from comercial.models import Marca


class MarcaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Marca
        fields = '__all__'
        widgets = {
            'ativo': forms.CheckboxInput()
        }        

    def save(self, commit=True):
        
        instance = super().save(commit=False)
        instance.credenciado = self.request.user.credenciado.pk

        if commit:
            instance.save()

        return instance