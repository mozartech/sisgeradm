from django.contrib.auth.decorators import login_required
from django.db import connection
from django.urls import reverse_lazy
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from comercial.models import (
    Cliente, ClienteMarca, ClienteVendedor,
    Canal, Contato, Marca, Segmento, Status, Grupo, Vendedor
)

from base.utils import dictfetchall, get_mes_nome


@login_required
def GerencialDashboard(request):
    
    cliente_total = Cliente.objects.filter(
        credenciado=request.user.credenciado.pk,
        ativo=True
    ).count()
    
    canais = Canal.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    segmentos = Segmento.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    status = Status.objects.filter(
        credenciado=request.user.credenciado.pk
    ).order_by('nome')
    grupos = Grupo.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    Vendedores = Vendedor.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    contexto = {
        'canais': canais,
        'segmentos': segmentos,
        'status': status,
        'grupos': grupos,
        'marcas': marcas,
        'vendedores': Vendedores,
        'cliente_total': cliente_total
    }

    return render(request, "comercial/gerencial_dashboard.html", contexto)


@login_required
def GerencialClienteCanal(request, codigo):
    content = {}
    if request.method == 'GET':
        clientes = Cliente.objects.filter(credenciado=request.user.credenciado.pk,
                                          canal=codigo,
                                          ativo=True).count()
        content['codigo'] = int(codigo)
        content['total'] = clientes   
    return JsonResponse(content)


@login_required
def GerencialClienteSegmento(request, codigo):
    content = {}
    if request.method == 'GET':
        clientes = Cliente.objects.filter(credenciado=request.user.credenciado.pk,
                                          segmento=codigo,
                                          ativo=True).count()
        content['codigo'] = int(codigo)
        content['total'] = clientes   
    return JsonResponse(content)


@login_required
def GerencialClienteStatus(request, codigo):
    content = {}
    if request.method == 'GET':
        clientes = Cliente.objects.filter(
            credenciado=request.user.credenciado.pk,
            status=codigo,
            ativo=True
        ).count()
        content['codigo'] = int(codigo)
        content['total'] = clientes   
    return JsonResponse(content)


@login_required
def GerencialClienteGrupo(request, codigo):
    content = {}
    if request.method == 'GET':
        clientes = Cliente.objects.filter(
            credenciado=request.user.credenciado.pk,
            grupo=codigo,
            ativo=True
        ).count()
        content['codigo'] = int(codigo)
        content['total'] = clientes   
    return JsonResponse(content)


@login_required
def GerencialClienteMarca(request, codigo):
    content = {}
    if request.method == 'GET':
        clientes = ClienteMarca.objects.filter(
                                          credenciado=request.user.credenciado.pk,
                                          marca_id=codigo).count()
        content['codigo'] = int(codigo)
        content['total'] = clientes   
    return JsonResponse(content)


@login_required
def GerencialClienteVendedor(request, codigo):
    content = {}
    if request.method == 'GET':
        clientes = ClienteVendedor.objects.filter(
                                          credenciado=request.user.credenciado.pk,
                                          vendedor_id=codigo
                                        ).count()
        content['codigo'] = int(codigo)
        content['total'] = clientes   
    return JsonResponse(content)


@login_required
def GerencialPesquisaCliente(request):

    contatos = Contato.objects.filter(credenciado=request.user.credenciado.pk)
    vendedores = Vendedor.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    marcas = Marca.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    canais = Canal.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    segmentos = Segmento.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    status = Status.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')
    grupos = Grupo.objects.filter(credenciado=request.user.credenciado.pk).order_by('nome')

    contexto = {
        'contatos': contatos,
        'vendedores': vendedores,
        'marcas': marcas,
        'canais': canais,
        'segmentos': segmentos,
        'status': status,
        'grupos': grupos
    }

    return render(request, "comercial/gerencial_pesquisa_cliente.html", contexto)


@login_required
def GerencialResumoVenda(request, ano):

    if int(ano) == 0:
        ano = timezone.now().year

    sql = '''
        select
            cast(EXTRACT(MONTH FROM p.data) as int) as mes,
            count(*) as qtde,
            count(distinct p.cliente_id) as cliente,
            sum(valor) as total
        from pedido p
        where
	        EXTRACT(year FROM p.data) = %s
        group by
	        EXTRACT(MONTH FROM p.data)
        union all
        select
            99 as mes,
            count(*) as qtde,
            count(distinct p.cliente_id) as cliente,
            sum(valor) as total
        from pedido p
        where
            EXTRACT(year FROM p.data) = %s
        order by 1
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(sql, [ano, ano])
        resumo_mes = dictfetchall(cursor)

    total_geral = 0.0

    for item in resumo_mes:
        total = item['total']
        if total is None:
            valor = 'R$ 0,00'
        else:    
            valor = "R$ {:,.2f}".format(total).replace(",", "X").replace(".", ",").replace("X", ".")
        item['valor'] = valor

        if item['mes'] == 99:
            total_geral = total
            item['nome'] = 'TOTAL'
        else:
            item['nome'] = get_mes_nome(item['mes'])

    for item in resumo_mes:
        total = item['total']
        if total and total_geral:
            item['progresso'] = int(round(total/total_geral*100))
        else:
            item['progresso'] = 0

    sql = '''
        select 
            c.nome,
            count(*) as qtde,
            sum(valor) as total
        from pedido p
        left join cliente c on (p.cliente_id = c.id)
        where
            EXTRACT(year FROM p.data) = %s
        group by
            c.nome
        union all
        select 
            'TOTAL' as nome,
            count(*) as qtde,
            sum(valor) as total
        from pedido p
        left join cliente c on (p.cliente_id = c.id)
        where
            EXTRACT(year FROM p.data) = %s
    '''

    with connection.cursor() as cursor:
        cursor.execute(sql, [ano, ano])
        resumo_cliente = dictfetchall(cursor)

    total_geral = 0.0

    for item in resumo_cliente:
        total = item['total']
        if total is None:
            valor = 'R$ 0,00'
        else:
            valor = "R$ {:,.2f}".format(total).replace(",", "X").replace(".", ",").replace("X", ".")
        item['valor'] = valor

        if item['nome'] == 'TOTAL':
            total_geral = total

    for item in resumo_cliente:
        total = item['total']
        if total and total_geral:
            item['progresso'] = int(round(total/total_geral*100))
        else:
            item['progresso'] = 0

    sql = '''
        select
            cc.estado_nome as nome,
            count(*) as qtde,
            count(distinct p.cliente_id) as cliente,
            sum(valor) as total
        from pedido p
        left join cliente c on (p.cliente_id = c.id)
        left join cidade cc on (cc.nome = c.endereco_cidade and cc.uf = c.endereco_uf)
        where
            EXTRACT(year FROM p.data) = %s
        group by
            cc.estado_nome
        union all
        select
            'TOTAL' as nome,
            count(*) as qtde,
            count(distinct p.cliente_id) as cliente,
            sum(valor) as total
        from pedido p
        left join cliente c on (p.cliente_id = c.id)
        left join cidade cc on (cc.nome = c.endereco_cidade and cc.uf = c.endereco_uf)
        where
            EXTRACT(year FROM p.data) = %s
    '''

    with connection.cursor() as cursor:
        cursor.execute(sql, [ano, ano])
        resumo_estado = dictfetchall(cursor)

    total_geral = 0.0

    for item in resumo_estado:
        total = item['total']
        if total is None:
            valor = 'R$ 0,00'
        else:
            valor = "R$ {:,.2f}".format(total).replace(",", "X").replace(".", ",").replace("X", ".")
        item['valor'] = valor

        if item['nome'] == 'TOTAL':
            total_geral = total

    for item in resumo_estado:
        total = item['total']
        if total and total_geral:
            item['progresso'] = int(round(total/total_geral*100))
        else:
            item['progresso'] = 0

    contexto = {
        'ano': int(ano),
        'resumo_mes': resumo_mes,
        'resumo_cliente': resumo_cliente,
        'resumo_estado': resumo_estado
    }

    return render(request, "gerencial/resumo_venda.html", contexto)