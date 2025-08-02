from base import __version__


def theme_dark(request, value):
    if request.user.is_authenticated and request.user.tema.find('dark') > -1:
        return value
    else:
        return ''


def bg_dark(request):
    if request.user.is_authenticated and request.user.tema.find('dark') > -1:
        return 'bg-dark'
    else:
        return 'bg-light'


def educatize_version(request):
    return {
        'versao': __version__,
        'btn_dark': theme_dark(request, 'btn-dark'),
        'bg_dark': bg_dark(request),
        'table_dark': theme_dark(request, 'table-dark'),
    }
