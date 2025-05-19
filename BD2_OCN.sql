ALTER TABLE public."Agenda"
ADD COLUMN "IDServicos" integer;

-- Adicionar a constraint de chave estrangeira para IDServicos
ALTER TABLE public."Agenda"
ADD CONSTRAINT fk_agenda_servico FOREIGN KEY ("IDServicos")
    REFERENCES public."Servicos" ("ID") MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

-- Corrigir o nome da coluna Descircao para Descricao (opcional, se quiser renomear)
ALTER TABLE public."Servicos"
RENAME COLUMN "Descircao" TO "Descricao";