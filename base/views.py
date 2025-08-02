from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone

'''
from allauth.account.view import PasswordChangeView

@login_required
class MyPasswordChangeView(PasswordChangeView):

    def get_context_data(self, **kwargs):
        ret = super(PasswordChangeView, self).get_context_data(**kwargs)
        ret["pretitle"] = 'Alterar Senha' 
        return ret
'''

def LogoutView(request):
    return render(request, 'account/logout.html', {})

'''
@login_required
def ChangePasswordView(request):
    pretitle = 'Alterar Senha'
    return render(request, 'account/password_change.html', locals())
'''

@login_required
def IndexView(request):
    title = 'Home'
    return render(request, 'base/home.html', locals())


def handler404(request):
    response = render(request, 'base/404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, 'base/500.html', {})
    response.status_code = 500
    return response
