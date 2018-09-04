list_detalhes_query = """
    select 
    MMPM_ORDEM,
    MMPM_MAPA_CRAAI,
    MMPM_MAPA_FORUM,
    MMPM_MAPA_BAIRRO,
    MMPM_MAPA_MUNICIPIO,
    MMPM_CRAAI,
    MMPM_COMARCA,
    MMPM_FORO,
    MMPM_GRUPO,
    MMPM_ORGAO,
    MMPM_TELEFONESORGAO,
    MMPM_EXIBEGRUPO,
    MMPM_EXIBEFORO,
    MMPM_ORDEMGRUPO,
    MMPM_ORDEMQUADRO,
    MMPM_MATRICULA,
    MMPM_NOME,
    MMPM_CELULAR,
    MMPM_CARGO,
    MMPM_CONCURSO,
    MMPM_ANOCONCURSO,
    MMPM_ROMANO,
    MMPM_FUNCAO,
    MMPM_ORDEMSUBSTITUCAO,
    MMPM_FLAG_PGJ,
    MMPM_FLAG_ELEITORAL,
    MMPM_FLAG_CRAAI,
    MMPM_DIAS,
    nvl(MMPM_AFASTAMENTO,'') as MMPM_AFASTAMENTO,
    MMPM_PGJ_FUNCAO,
    MMPM_DTNASC,
    MMPM_DTINICIOSUBS,
    MMPM_DTFIMSUBS,
    MMPM_FLAG_ASSESSOR,
    MMPM_CDORGAO
    from MMPS.MMPS_ADM_RH_MOV_PROM
    where mmpm_cdorgao = :org
    order by MMPM_ORDEM, MMPM_ORDEMSUBSTITUCAO   
""" 

list_orgaos_query = """
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

list_vistas_query = """
    SELECT
        NVL(COUNT(TOTAL), 0) TOTAL,
        NVL(COUNT(HOJE), 0) HOJE,
        NVL(COUNT(ATE_30), 0) ATE_30,
        NVL(COUNT(DE_30_A_40), 0) DE_30_A_40,
        NVL(COUNT(MAIS_40), 0) MAIS_40
    FROM(
        SELECT
            1 TOTAL,
            CASE
                WHEN FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) < 1
                    AND FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) >= 0
                THEN 1
            END AS HOJE,
            CASE
                WHEN FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) <= 30
                    AND FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) >= 0
                THEN 1
            END AS ATE_30,
            CASE
                WHEN FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) <= 40
                    AND FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) > 30
                THEN 1
            END AS DE_30_A_40,
            CASE
                WHEN FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) > 40
                THEN 1
            END AS MAIS_40
        FROM
            MCPR_VISTA
            JOIN MCPR_DOCUMENTO ON DOCU_DK = VIST_DOCU_DK
        WHERE
            (DOCU_ORGI_ORGA_DK_RESPONSAVEL = :org
                OR DOCU_ORGI_ORGA_DK_CARGA = :org)
            AND VIST_DT_FECHAMENTO_VISTA IS NULL
            AND DOCU_TPST_DK != 11
        ORDER BY 1 DESC
    )
"""