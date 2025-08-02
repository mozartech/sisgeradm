from django.core.exceptions import ValidationError

from bradocs4py import cpf, cnpj


def int_to_bool(value):
    if value == '':
        return False
    else:
        return bool(int(value))

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
    from unicodedata import normalize
    return normalize(u'NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

def clear_format(value):
    texto = value if value else ''
    for s in ['.', ',', '-', '/', '(', ')', ' ']:
        texto = texto.replace(s, '')
    return texto

def is_ddmmyyyy(text):
    return len(text) == 10 and text[2] in ['/','-'] and text[5] in ['/','-']

def to_yyyymmdd(text):
    if '/' in text:
        l = text.split('/')
    else:
        l = text.split('-')
    l.reverse()
    return '-'.join(l)

def date_yyyymmdd(data):
    return to_yyyymmdd(data)

def copy_digit(value):
    texto = ''
    for c in value:
        if c.isdigit():
            texto += c
    return texto
