--Captação líquida acumulada por mês 
WITH aux AS(
SELECT 
CASE
	  WHEN flag_subclasse = 1 THEN id_subclasse
	  WHEN flag_subclasse = 0 THEN cnpj_fundo_classe
	  END AS id_fundo
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
where id_fundo = '11.233.045/0001-22'
GROUP BY mes, id_fundo
ORDER BY id_fundo, mes
;

--TOP 10 fundos por Captação líquida acumulada no mês 
WITH aux AS(
SELECT 
cnpj_fundo_classe
,id_subclasse
,CASE
	  WHEN flag_subclasse = 1 THEN id_subclasse
	  WHEN flag_subclasse = 0 THEN cnpj_fundo_classe
	  END AS id_fundo
,flag_subclasse
,CAST(DATE_TRUNC('month', dt_comptc)AS DATE) AS mes
,captc_dia
,resg_dia
FROM dados_abertos_cvm.informe_diario_fundos  
)
SELECT 
 mes
,id_fundo
,SUM(captc_dia - resg_dia) AS captacao_liquida_mensal

FROM aux
WHERE mes = '2025-08-01' 
GROUP BY mes, id_fundo
ORDER BY captacao_liquida_mensal DESC
LIMIT 10
;

-- Top 10 fundos por Patrimônio líquido em uma data específica
WITH aux AS(
SELECT 
CASE
	  WHEN flag_subclasse = 1 THEN id_subclasse
	  WHEN flag_subclasse = 0 THEN cnpj_fundo_classe
	  END AS id_fundo
,vl_total
,dt_comptc
FROM dados_abertos_cvm.informe_diario_fundos
)
SELECT 
    id_fundo,
    MAX(vl_total) AS patrimonio_liquido
FROM aux
WHERE dt_comptc = '2025-08-29' -- No SQL Server eu poderia usar uma variável para que essa data seja sempre o último dia útil do mês anterior
GROUP BY id_fundo
ORDER BY patrimonio_liquido DESC
LIMIT 10
;

--Top 10 fundos com maior número de cotistas em uma data específica
WITH aux AS(
SELECT 
CASE
	  WHEN flag_subclasse = 1 THEN id_subclasse
	  WHEN flag_subclasse = 0 THEN cnpj_fundo_classe
	  END AS id_fundo
,nr_cotst
,dt_comptc
FROM dados_abertos_cvm.informe_diario_fundos
)
SELECT 
    id_fundo,
    MAX(nr_cotst) AS num_cotistas
FROM aux
WHERE dt_comptc = '2025-08-29' -- No SQL Server eu poderia usar uma variável para que essa data seja sempre o último dia útil do mês anterior
GROUP BY id_fundo
ORDER BY num_cotistas DESC
LIMIT 10
;

--Evolução do Patrimônio Líquido de um fundo
WITH aux AS(
SELECT 
CASE
	  WHEN flag_subclasse = 1 THEN id_subclasse
	  WHEN flag_subclasse = 0 THEN cnpj_fundo_classe
	  END AS id_fundo
,vl_total
,dt_comptc
FROM dados_abertos_cvm.informe_diario_fundos
)
SELECT 
id_fundo
,dt_comptc
,vl_total AS patrimonio_liquido
FROM aux
WHERE id_fundo = '07.593.972/0001-86'
ORDER BY dt_comptc
;

--Retorno Diário de um fundo
WITH aux AS(
SELECT 
CASE
	  WHEN flag_subclasse = 1 THEN id_subclasse
	  WHEN flag_subclasse = 0 THEN cnpj_fundo_classe
	  END AS id_fundo
,vl_quota
,dt_comptc
FROM dados_abertos_cvm.informe_diario_fundos
)
SELECT 
    dt_comptc,
    vl_quota,
    LAG(vl_quota) OVER (PARTITION BY id_fundo ORDER BY dt_comptc) AS vl_quota_anterior,
    ROUND((vl_quota / LAG(vl_quota) OVER (PARTITION BY id_fundo ORDER BY dt_comptc) - 1) * 100, 2) AS retorno_diario_pct
FROM aux
WHERE id_fundo = '07.593.972/0001-86'
ORDER BY dt_comptc
;

select * from dados_abertos_cvm.informe_diario_fundos  
where cnpj_fundo_classe = '11.233.045/0001-22'
order by dt_comptc