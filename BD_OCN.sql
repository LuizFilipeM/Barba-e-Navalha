CREATE TYPE public.tipo_usuario_enum AS ENUM ('Cliente', 'Barbeiro');

CREATE TABLE public."Usuario"
(
    "ID" serial,
    "Email" character varying(255),
    "Senha" character varying(255),
    "Tipo" tipo_usuario_enum,
    PRIMARY KEY ("ID")
);

ALTER TABLE IF EXISTS public."Usuario"
    OWNER to "navalha";

CREATE TABLE public."Cliente"
(
    "ID" integer,
    "CPF" character varying(14),
    "Nome" character varying(255),
    "Cidade" character varying(255),
    "Telefone" character varying(16),
    "Data_Nascimento" date,
    PRIMARY KEY ("ID"),
    CONSTRAINT fk_usuario_paciente FOREIGN KEY ("ID")
        REFERENCES public."Usuario" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public."Cliente"
    OWNER to "navalha";

CREATE TABLE public."Barbeiro"
(
    "ID" integer,
    "Nome" character varying(255),
    "CPF" character varying(14),
    "Telefone" character varying(16),
    "Data_Nascimento" date,
    "Cidade" character varying(255),
    PRIMARY KEY ("ID"),
    CONSTRAINT fk_usuario_profissional FOREIGN KEY ("ID")
        REFERENCES public."Usuario" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public."Barbeiro"
    OWNER to "navalha";

CREATE TABLE public."Agenda"
(
    "ID" serial,
    "Data" date,
    "Hora" decimal(4,2),
    "IDBarbeiro" integer,
    "IDCliente" integer,
    PRIMARY KEY ("ID"),
    CONSTRAINT fk_agenda_barbeiro FOREIGN KEY ("IDBarbeiro")
        REFERENCES public."Barbeiro" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT fk_agenda_cliente FOREIGN KEY ("IDCliente")
        REFERENCES public."Cliente" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public."Agenda"
    OWNER to "navalha";

CREATE TABLE public."Horarios"
(
    "ID" serial,
    "Dia_semana" char(7),
    "Hora_inicio" integer,
    "Hora_fim" integer,
    PRIMARY KEY ("ID")
);

ALTER TABLE IF EXISTS public."Horarios"
    OWNER to "navalha";

CREATE TABLE public."Servicos"
(
    "ID" serial,
    "Nome" character varying(255),
    "Descircao" character varying(255),
    "Preco" decimal(5,2),
    PRIMARY KEY ("ID")
);

ALTER TABLE IF EXISTS public."Servicos"
    OWNER to "navalha";

CREATE TABLE public."Local"
(
    "ID" serial,
    "Nome_local" character varying(255),
    "Endereco" character varying(255),
    "CNPJ" character varying(255),
    "Telefone" character varying(16),
    "IDHorarios" integer,
    "IDServicos" integer,
    "BarbeiroUsuarioID" integer,
    PRIMARY KEY ("ID"),
    CONSTRAINT fk_local_barbeiro FOREIGN KEY ("BarbeiroUsuarioID")
        REFERENCES public."Barbeiro" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT fk_local_horarios FOREIGN KEY ("IDHorarios")
        REFERENCES public."Horarios" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT fk_local_servicos FOREIGN KEY ("IDServicos")
        REFERENCES public."Servicos" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public."Local"
    OWNER to "navalha";
