DROP TABLE IF EXISTS metrics_executions;
DROP TABLE IF EXISTS results;

CREATE TABLE metrics_executions (
    id SERIAL PRIMARY KEY,
    model_id UUID NOT NULL UNIQUE,
    cron_expression VARCHAR NOT NULL
);

CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    model_id UUID NOT NULL,
    y_true JSON NOT NULL,
    y_pred JSON NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);


INSERT INTO results (model_id, y_true, y_pred)
VALUES
    ('6d6a8224-de68-4603-b2db-63e01d34f020', '[1, 0, 1, 1]', '[1, 0, 0, 1]'),
    ('6d6a8224-de68-4603-b2db-63e01d34f020', '[0, 1, 1, 0]', '[0, 1, 1, 1]'),
    ('30dc8119-afe0-4dbd-9555-eb36fa408fd4', '[1, 0, 1, 1]', '[1, 0, 0, 1]'),
    ('30dc8119-afe0-4dbd-9555-eb36fa408fd4', '[0, 1, 1, 0]', '[0, 1, 1, 1]'),
    ('30dc8119-afe0-4dbd-9555-eb36fa408fd4', '[1, 1, 0, 0]', '[1, 1, 0, 0]');
