import pandas

from flask import jsonify, request
from app import app
from database import DAO
from .orgaos_sql import (
    acervo_qtd_query,
    list_orgaos_query,
    list_acervo_query,
    list_detalhes_query,
    list_vistas_query,
    acervo_classe_pai_query)


@app.route("/api/orgaos", methods=['GET'])
def list_orgaos():
    data = DAO.run(list_orgaos_query)
    results = []
    for row in data:
        row_dict = {
            'CDORG': row[0],
            'CRAAI': row[1],
            'COMARCA': row[2],
            'FORO': row[3],
            'ORGAO': row[4],
            'TITULAR': row[5],
        }
        results.append(row_dict)
    return jsonify(results)


@app.route("/api/orgaos/vistas", methods=['GET'])
def list_vistas():
    cdorg = request.args.get('cdorg')
    data = DAO.run(list_vistas_query, {'org': cdorg})
    results = []
    for row in data:
        row_dict = {
            'TOTAL': row[0],
            'HOJE': row[1],
            'ATE_30': row[2],
            'DE_30_A_40': row[3],
            'MAIS_40': row[4],
        }
        results.append(row_dict)
    return jsonify(results)


@app.route("/api/orgaos/acervo", methods=['GET'])
def list_acervo():
    cdorg = request.args.get('cdorg')
    acervo = DAO.run(acervo_qtd_query, {'org': cdorg}).fetchone()[0]
    meses = DAO.run(list_acervo_query, {'org': cdorg}).fetchall()

    result = {"ACERVO_ATUAL": acervo}
    historico = []
    prev_acervo = acervo
    for mes in meses:
        acervo_fim_mes = prev_acervo
        entradas = mes[1]
        saidas = mes[2]
        saldo = entradas - saidas
        acervo_inicio_mes = acervo_fim_mes - saldo  # Olhando para trás

        mes_dict = {
            'MES': mes[0],
            'ENTRADAS': entradas,
            'SAIDAS': saidas,
            'ACERVO_FIM_MES': acervo_fim_mes,
            'SALDO': saldo,
            'ACERVO_INICIO_MES': acervo_inicio_mes
        }

        historico.append(mes_dict)
        prev_acervo = acervo_inicio_mes

    result['HISTORICO'] = historico
    return jsonify(result)


def get_designacao(arr):
    return [
        (
            a['MMPM_MATRICULA'],
            a['MMPM_NOME'],
            a['MMPM_FUNCAO'],
            a['MMPM_DTINICIOSUBS'],
            a['MMPM_DTFIMSUBS']
        )
        for a in arr
    ]


@app.route("/api/orgaos/detalhes", methods=['GET'])
def list_detalhes():
    cdorg = request.args.get('cdorg')
    data = list(DAO.run(list_detalhes_query, {'org': cdorg}))

    colunas = """MMPM_ORDEM
                MMPM_MAPA_CRAAI
                MMPM_MAPA_FORUM
                MMPM_MAPA_BAIRRO
                MMPM_MAPA_MUNICIPIO
                MMPM_CRAAI
                MMPM_COMARCA
                MMPM_FORO
                MMPM_GRUPO
                MMPM_ORGAO
                MMPM_TELEFONESORGAO
                MMPM_EXIBEGRUPO
                MMPM_EXIBEFORO
                MMPM_ORDEMGRUPO
                MMPM_ORDEMQUADRO
                MMPM_MATRICULA
                MMPM_NOME
                MMPM_CELULAR
                MMPM_CARGO
                MMPM_CONCURSO
                MMPM_ANOCONCURSO
                MMPM_ROMANO
                MMPM_FUNCAO
                MMPM_ORDEMSUBSTITUCAO
                MMPM_FLAG_PGJ
                MMPM_FLAG_ELEITORAL
                MMPM_FLAG_CRAAI
                MMPM_DIAS
                MMPM_AFASTAMENTO
                MMPM_PGJ_FUNCAO
                MMPM_DTNASC
                MMPM_DTINICIOSUBS
                MMPM_DTFIMSUBS
                MMPM_FLAG_ASSESSOR
                MMPM_CDORGAO
                """.split("\n")

    colunas = [c.strip() for c in colunas]
    data = [dict(zip(colunas, d)) for d in data]

    if not data:
        return jsonify({})

    retorno = {
        "detalhes": {
            "MATRICULA": data[0]["MMPM_MATRICULA"],
            "NOME": data[0]["MMPM_NOME"],
            "CARGO": data[0]["MMPM_CARGO"],
            "CONCURSO": data[0]["MMPM_CONCURSO"],
            "ANOCONCURSO": data[0]["MMPM_ANOCONCURSO"],
            "ROMANO": data[0]["MMPM_ROMANO"],
            "FLAG_PGJ": data[0]["MMPM_FLAG_PGJ"],
            "FLAG_ELEITORAL": data[0]["MMPM_FLAG_ELEITORAL"],
            "FLAG_CRAAI": data[0]["MMPM_FLAG_CRAAI"],
            "DTNASC": data[0]["MMPM_DTNASC"],
            "FLAG_ASSESSOR": data[0]["MMPM_FLAG_ASSESSOR"],
            "CDORGAO": data[0]["MMPM_CDORGAO"],
            "TELEFONESORGAO": data[0]["MMPM_TELEFONESORGAO"].split(' | ')[1:],
            "ORGAO": data[0]["MMPM_ORGAO"],
            "CELULAR": data[0]["MMPM_CELULAR"],
        },
        "funcoes": data[0]["MMPM_PGJ_FUNCAO"].split('@'),
        "designacoes": get_designacao(data[1:]),
        "afastamento": (data[0]["MMPM_AFASTAMENTO"].split('@')
                        if data[0]["MMPM_AFASTAMENTO"] else [])
    }

    return jsonify(retorno)


@app.route("/api/orgaos/acervoClasse", methods=['GET'])
def list_acervo_classe():
    cdorg = request.args.get('cdorg')
    data = DAO.run(acervo_classe_pai_query, {'org': cdorg})
    results = []
    for row in data:
        row_dict = {
            'CLASSE_ID_PAI': row[0],
            'CLASSE_PAI': row[1],
            'QTD': row[2]
        }
        results.append(row_dict)
    return jsonify(results)


@app.route("/api/orgaos/financeiro", methods=['GET'])
def financeiro():
    cdorg = int(request.args.get('cdorg'))
    consolidados = pandas.read_csv(
        'model/sheets/consolidacao.csv', sep=';',
        converters={'Total': format_money,
                    'Área do Layout': to_float}
    )
    orgaos = pandas.read_csv('model/sheets/orgaos.csv', sep=';')
    imoveis = pandas.read_csv('model/sheets/imoveis.csv', sep=';')

    nome_promotoria = (
        orgaos[orgaos['Código do Órgão'] == cdorg]
        ['Nome do Órgão'].values
    )

    if nome_promotoria.size == 0:
        return {}

    df_orgao = (
        consolidados[consolidados['Centro de Custos'] == nome_promotoria[0]]
    )
    area_orgao = df_orgao['Área do Layout'].values[0]
    custo = df_orgao['Total'].sum()
    codigo_imovel = df_orgao['Código do Imóvel'].values[0]
    natureza = (
        imoveis[imoveis['CÓDIGO'] == codigo_imovel]['NATUREZA'].values[0]
    )

    return jsonify({
        'custo_orgao': custo,
        'area_orgao': area_orgao,
        'natureza': natureza
    })


@app.route("/api/orgaos/financeiro/agrupado", methods=['GET'])
def financeiro_agrupado():
    cdorg = int(request.args.get('cdorg'))
    consolidados = pandas.read_csv(
        'model/sheets/consolidacao.csv', sep=';',
        converters={'Total': format_money,
                    'Área do Layout': to_float}
    )
    orgaos = pandas.read_csv('model/sheets/orgaos.csv', sep=';')

    if orgaos[orgaos['Código do Órgão'] == cdorg]['Nome do Órgão'] \
            .values.size == 0:
        return {}

    nome_promotoria = (
        orgaos[orgaos['Código do Órgão'] == cdorg]['Nome do Órgão'].values[0]
    )

    df_orgao = (
        consolidados[consolidados['Centro de Custos'] == nome_promotoria]
    )

    return jsonify(df_orgao.groupby('Tipo de Custo').Total.sum().to_dict())


def to_float(val):
    try:
        return float(val.replace(',', '.'))
    except ValueError:
        return 0


def format_money(val):
    try:
        val = val.replace('R$', '').replace('.', '').replace(',', '.')
        return float(val)
    except ValueError:
        return 0
