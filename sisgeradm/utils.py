import re
from datetime import datetime

from comercial.models import Cliente


def csv_to_cliente(file_from):

    file_new = []  # contém as linhas para o novo arquivo

    arquivo = 'C:/educatize-web/sisgeradm/static/' + file_from

    with open(arquivo) as file:
        
        for line in file:

            linha = line.strip()

            if linha == '':
                continue

            lista = linha.split(',')

            for k, v in enumerate(lista):
                lista[k] = v.strip()

            _, nome, cnpj, codigo, inscricao, telefone, email, instagram, cadastro = lista
            
            if cnpj == '':
                continue

            cnpj = ''.join(re.findall(r'\d+', cnpj))

            try:
                cliente = Cliente.objects.get(chave=cnpj)
                cliente.cnpj = cnpj
            except Cliente.DoesNotExist:
                cliente = Cliente()
                cliente.cnpj = cnpj
                cliente.credenciado = 1

            nome = nome.replace('  ', ' ')
            if nome[-1] == '.':
                nome = nome[:-1]

            if len(codigo) > 10:
                codigo = ''

            inscricao = ''.join(re.findall(r'\d+', inscricao))

            if len(inscricao) != 9:
                inscricao = ''

            telefone = ''.join(re.findall(r'\d+', telefone))

            telefone_fixo  = ''
            telefone_movel = ''

            if telefone.isdigit():   # somente numeros

                ddd, numero = telefone[0:2], telefone[2:]
                if numero[0] in ['8','9'] and len(numero) == 8: # 81657770
                    numero = '9'+numero

                if numero[0] == '9':
                    telefone_movel = '('+ddd+') '+numero[0:5]+'-'+numero[5:]
                else:
                    telefone_fixo = '('+ddd+') '+numero[0:4]+'-'+numero[4:]

            cliente.nome = nome.upper()
            cliente.codigo = codigo
            cliente.inscricao_estadual = inscricao
            cliente.telefone_1 = telefone_fixo
            cliente.telefone_2 = telefone_movel
            cliente.email = email.lower()
            cliente.instagram = instagram.lower()

            cliente.cadastro = datetime.strptime(cadastro, '%Y-%m-%d %H:%M:%S')

            cliente.save()
