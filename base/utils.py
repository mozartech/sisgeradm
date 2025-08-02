import unicodedata

from django.core.exceptions import ValidationError

from bradocs4py import cpf, cnpj


def validate_cpf(value):
    if value and not cpf.CPF(value).isValid:
        raise ValidationError('O CPF não é válido.')


def _validate_cpf(value):
    return value and cpf.CPF(value).isValid
        

def validate_cnpj(value):
    if value and not cnpj.Cnpj(value).isValid:
        raise ValidationError('O CNPJ não é válido.')


def _validate_cnpj(value):
    return value and cnpj.Cnpj(value).isValid


def clear_text(text):
    return unicodedata.normalize(u'NFKD', text).encode('ascii', 'ignore').decode('ASCII')


def clear_format(value):
    texto = value if value else ''
    for s in ['.', ',', '-', '/', '(', ')', ' ']:
        texto = texto.replace(s, '')
    return texto


def date_yyyymmdd(data):
    l = data.split('/')
    l.reverse()
    return '-'.join(l)

def copy_digit(value):
    texto = ''
    for c in value:
        if c.isdigit():
            texto += c
    return texto


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0].lower() for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_mes_nome(mes):

    MESES = [
        'JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO','JUNHO',
        'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'
    ]

    return MESES[mes-1]