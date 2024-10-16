from flask import Flask, request, jsonify
from celery import Celery
from redbeat import RedBeatSchedulerEntry
from celery.schedules import crontab
import psycopg2
import redis
import uuid

app = Flask(__name__)

DATABASE = {
    'host': 'postgres',
    'database': 'mydatabase',
    'user': 'user',
    'password': 'password'
}

REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DB = 0

app.config['CELERY_BROKER_URL'] = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
app.config['CELERY_RESULT_BACKEND'] = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.beat_scheduler = 'redbeat.RedBeatScheduler'

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.get_json()
    model_id = data.get('model_id')
    cron_expression = data.get('cron_expression')

    try:
        model_uuid = uuid.UUID(model_id)
    except ValueError:
        return jsonify({'error': 'Invalid model_id format. Must be a valid UUID.'}), 400

    conn = psycopg2.connect(**DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM metrics_executions WHERE model_id = %s;", (str(model_uuid),))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("DELETE FROM metrics_executions WHERE model_id = %s;", (str(model_uuid),))
        conn.commit()
        remove_task(str(model_uuid))

    cursor.execute(
        "INSERT INTO metrics_executions (model_id, cron_expression) VALUES (%s, %s);",
        (str(model_uuid), cron_expression)
    )
    conn.commit()

    add_task(str(model_uuid), cron_expression)

    cursor.close()
    conn.close()

    return jsonify({'status': 'scheduled'}), 200

@app.route('/results/<model_id>', methods=['GET'])
def get_results(model_id):
    try:
        model_uuid = uuid.UUID(model_id)
    except ValueError:
        return jsonify({'error': 'Invalid model_id format. Must be a valid UUID.'}), 400

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    result = r.get(f'result_{model_uuid}')
    if result:
        return jsonify({'model_id': str(model_uuid), 'accuracy': float(result)}), 200
    else:
        return jsonify({'error': 'No results found'}), 404

def add_task(model_id, cron_expression):
    cron_parts = cron_expression.strip().split(' ')
    if len(cron_parts) != 5:
        raise ValueError('Invalid cron expression format.')

    schedule = crontab(minute=cron_parts[0], hour=cron_parts[1], day_of_month=cron_parts[2],
                       month_of_year=cron_parts[3], day_of_week=cron_parts[4])

    entry = RedBeatSchedulerEntry(name=f'task_{model_id}',
                                  task='tasks.calculate_accuracy',
                                  schedule=schedule,
                                  args=[model_id],
                                  app=celery)
    entry.save()

def remove_task(model_id):
    try:
        entry = RedBeatSchedulerEntry.from_key(f'redbeat:task_{model_id}', app=celery)
        entry.delete()
    except KeyError:
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
