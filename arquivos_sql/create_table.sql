-- Table: dados_abertos_cvm.informe_diario_fundos

-- DROP TABLE IF EXISTS dados_abertos_cvm.informe_diario_fundos;

CREATE TABLE IF NOT EXISTS dados_abertos_cvm.informe_diario_fundos
(
    tp_fundo_classe VARCHAR(15) COLLATE pg_catalog."default",
    cnpj_fundo_classe VARCHAR(20) COLLATE pg_catalog."default" NOT NULL,
    id_subclasse VARCHAR(15) COLLATE pg_catalog."default" NOT NULL,
    dt_comptc DATE NOT NULL,
    vl_total NUMERIC,
    vl_quota NUMERIC,
    vl_patrim_liq NUMERIC,
    captc_dia NUMERIC,
    resg_dia NUMERIC,
    nr_cotst INT,
    flag_subclasse INT NOT NULL,
    CONSTRAINT informe_diario_fundos_pk PRIMARY KEY (cnpj_fundo_classe, id_subclasse, dt_comptc),
    CONSTRAINT informe_diario_fundos_unique UNIQUE (cnpj_fundo_classe, id_subclasse, dt_comptc)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS dados_abertos_cvm.informe_diario_fundos
    OWNER to postgres;

REVOKE ALL ON TABLE dados_abertos_cvm.informe_diario_fundos FROM eduardan;

GRANT INSERT, DELETE, SELECT, UPDATE ON TABLE dados_abertos_cvm.informe_diario_fundos TO eduardan;

GRANT ALL ON TABLE dados_abertos_cvm.informe_diario_fundos TO postgres;