select * from dados_abertos_cvm.informe_diario_fundos limit 10
-- where id_subclasse <> 'Não se aplica'

select distinct dt_comptc from dados_abertos_cvm.informe_diario_fundos

select count(cnpj_fundo_classe) from dados_abertos_cvm.informe_diario_fundos


SELECT 
    dt_comptc,
    vl_total AS patrimonio_liquido
FROM dados_abertos_cvm.informe_diario_fundos
WHERE cnpj_fundo_classe = '45.121.329/0001-49'
ORDER BY dt_comptc
;

SELECT 
    dt_comptc,
    vl_quota,
    LAG(vl_quota) OVER (PARTITION BY cnpj_fundo_classe ORDER BY dt_comptc) AS vl_quota_anterior,
    ROUND((vl_quota / LAG(vl_quota) OVER (PARTITION BY cnpj_fundo_classe ORDER BY dt_comptc) - 1) * 100, 2) AS retorno_diario_pct
FROM dados_abertos_cvm.informe_diario_fundos
WHERE cnpj_fundo_classe = '45.121.329/0001-49'
ORDER BY dt_comptc
;

SELECT 
    cnpj_fundo_classe,
    MAX(vl_total) AS patrimonio_liquido
FROM dados_abertos_cvm.informe_diario_fundos
WHERE dt_comptc = '2025-08-22'
GROUP BY cnpj_fundo_classe
ORDER BY patrimonio_liquido DESC
LIMIT 10
;
--Captação líquida acumulada por mês 

WITH aux AS(
SELECT 
cnpj_fundo_classe
,id_subclasse
,CASE
	  WHEN flag_subclasse = 1 THEN id_subclasse
	  WHEN flag_subclasse = 0 THEN cnpj_fundo_classe
	  END AS id_fundo
,flag_subclasse
,DATE_TRUNC('month', dt_comptc) AS mes
,captc_dia
,resg_dia
FROM dados_abertos_cvm.informe_diario_fundos  
)
SELECT 
CAST(mes AS DATE)
,id_fundo
,SUM(captc_dia - resg_dia) AS captacao_liquida_mensal

FROM aux
GROUP BY mes, id_fundo
ORDER BY id_fundo, mes