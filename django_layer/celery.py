import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_layer.settings')

app = Celery('django_layer')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'update_cache': {
        'task': 'tasks.tasks.run_update_cache',
        'schedule': crontab(minute='*/1')
    },
}
