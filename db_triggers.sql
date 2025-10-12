-- Esquemas
CREATE SCHEMA IF NOT EXISTS audit;

-- Tabla de auditoría mínima (si quieres consultarla)
CREATE TABLE IF NOT EXISTS audit.change_log (
  id BIGSERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  table_name TEXT NOT NULL,
  op TEXT NOT NULL,
  user_name TEXT NOT NULL,
  pk JSONB,
  changed_cols TEXT[],
  old_row JSONB,
  new_row JSONB
);

-- Función para construir JSON de PK
CREATE OR REPLACE FUNCTION audit.pk_json(_rel regclass, _old JSONB, _new JSONB)
RETURNS JSONB
LANGUAGE plpgsql AS $$
DECLARE pk JSONB;
BEGIN
  SELECT jsonb_object_agg(a.attname, (CASE WHEN _new ? a.attname THEN _new ELSE _old END)->a.attname)
  INTO pk
  FROM pg_index i
  JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
  WHERE i.indrelid = _rel AND i.indisprimary;
  RETURN pk;
END $$;

-- Función NOTIFY + auditoría
CREATE OR REPLACE FUNCTION audit.on_change_notify()
RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
  tbl TEXT := TG_TABLE_SCHEMA||'.'||TG_TABLE_NAME;
  op  TEXT := TG_OP;
  changed_cols TEXT[];
  payload JSONB;
  pkj JSONB;
BEGIN
  IF op = 'UPDATE' THEN
    SELECT ARRAY(
      SELECT k FROM jsonb_each_text(to_jsonb(NEW))
      WHERE (to_jsonb(OLD)->>k) IS DISTINCT FROM (to_jsonb(NEW)->>k)
    )
    INTO changed_cols;
  END IF;

  pkj := audit.pk_json(TG_RELID, to_jsonb(OLD), to_jsonb(NEW));

  INSERT INTO audit.change_log(table_name, op, user_name, pk, changed_cols, old_row, new_row)
  VALUES (tbl, op, current_user, pkj, changed_cols, to_jsonb(OLD), to_jsonb(NEW));

  payload := jsonb_build_object(
    'ts', now(),
    'table', tbl,
    'op', op,
    'user', current_user,
    'pk', pkj,
    'changed_cols', COALESCE(to_jsonb(changed_cols), '[]'::jsonb),
    'old_row', to_jsonb(OLD),
    'new_row', to_jsonb(NEW)
  );

  PERFORM pg_notify('audit_events', payload::text);
  RETURN CASE WHEN op='DELETE' THEN OLD ELSE NEW END;
END $$;

-- EJEMPLO: aplicar a una tabla sensible (ajusta el nombre)
-- Si no tienes aún, puedes crear una tabla de ejemplo:
-- CREATE TABLE IF NOT EXISTS public.customers(
--   id SERIAL PRIMARY KEY,
--   email TEXT, role TEXT, status TEXT, credit_limit NUMERIC
-- );

DROP TRIGGER IF EXISTS tr_customers_after ON public.customers;
CREATE TRIGGER tr_customers_after
AFTER INSERT OR UPDATE OR DELETE ON public.customers
FOR EACH ROW EXECUTE FUNCTION audit.on_change_notify();
