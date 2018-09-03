from database import DAO

list_orgaos_query = f"""
    SELECT 
        org.ORLW_ORGI_CDORGAO AS CDORG,
        org.ORLW_REGI_NM_REGIAO AS CRAAI,
        org.ORLW_CMRC_NM_COMARCA AS COMARCA,
        org.ORLW_COFO_NM_FORO AS FORO,
        org.ORLW_ORGI_NM_ORGAO AS ORGAO,
        func.NMFUNCIONARIO AS TITULAR
    FROM 
        ORGI_VW_ORGAO_LOCAL_ATUAL org
        LEFT JOIN MPRJ_VW_FUNCIONARIO func ON func.CDORGAO = org.ORLW_DK
    WHERE
        1=1
        AND org.ORLW_TPOR_DK = 1
        AND (org.ORLW_ORGI_DT_FIM IS NULL
            OR org.ORLW_ORGI_DT_FIM > SYSDATE)
        AND func.CDTIPFUNC = 1 
        AND func.CDSITUACAOFUNC = 1
        AND func.CDCARGO = 74
"""


def list_orgaos():
    data = DAO.run(list_orgaos_query)
    results = []
    for row in data:
        row_dict = {
            "CDORG": row[0],
            "CRAAI": row[1],
            "COMARCA": row[2],
            "FORO": row[3],
            "ORGAO": row[4],
            "TITULAR": row[5]
        }
        results.append(row_dict)
    return results
