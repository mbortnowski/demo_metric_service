from celery import Celery
import psycopg2
import redis
from sklearn.metrics import accuracy_score

DATABASE = {
    'host': 'postgres',
    'database': 'mydatabase',
    'user': 'user',
    'password': 'password'
}

REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DB = 0

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')
celery.conf.beat_scheduler = 'redbeat.RedBeatScheduler'

@celery.task
def calculate_accuracy(model_id):
    conn = psycopg2.connect(**DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT y_true, y_pred FROM results
        WHERE model_id = %s
        ORDER BY timestamp DESC
        LIMIT 1;
    """, (model_id,))
    result = cursor.fetchone()

    if result:
        y_true, y_pred = result

        acc = accuracy_score(y_true, y_pred)

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        r.set(f'result_{model_id}', acc)
    else:
        print(f'No results found for model_id {model_id}')

    cursor.close()
    conn.close()
