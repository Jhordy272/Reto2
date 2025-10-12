-- Tabla principal de logs
CREATE TABLE IF NOT EXISTS app_logs (
  id           BIGSERIAL PRIMARY KEY,
  service      TEXT        NOT NULL,
  level        TEXT        NOT NULL,
  message      TEXT        NOT NULL,
  context      JSONB,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_app_logs_created_at ON app_logs (created_at);
CREATE INDEX IF NOT EXISTS idx_app_logs_level      ON app_logs (level);
CREATE INDEX IF NOT EXISTS idx_app_logs_service    ON app_logs (service);

-- 1) NOTIFY al insertar en app_logs
CREATE OR REPLACE FUNCTION notify_app_log() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE payload JSONB;
BEGIN
  payload := jsonb_build_object(
    'id', NEW.id,
    'ts', NEW.created_at,
    'service', NEW.service,
    'level', NEW.level,
    'message', NEW.message,
    'context', COALESCE(NEW.context, '{}'::jsonb)
  );
  PERFORM pg_notify('app_logs_events', payload::text);
  RETURN NEW;
END $$;

DROP TRIGGER IF EXISTS tr_app_logs_notify ON app_logs;
CREATE TRIGGER tr_app_logs_notify
AFTER INSERT ON app_logs
FOR EACH ROW EXECUTE FUNCTION notify_app_log();

-- 2) Tabla de hallazgos/insights (para el analizador)
CREATE TABLE IF NOT EXISTS log_insights (
  id BIGSERIAL PRIMARY KEY,
  detected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  service TEXT NOT NULL,
  rule TEXT NOT NULL,
  score DOUBLE PRECISION,
  sample_log_id BIGINT,
  sample_msg TEXT,
  context JSONB
);

CREATE INDEX IF NOT EXISTS idx_log_insights_detected_at ON log_insights(detected_at);
CREATE INDEX IF NOT EXISTS idx_log_insights_service     ON log_insights(service);
