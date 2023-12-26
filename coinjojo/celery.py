import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

app = Celery('coinjojo')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.timezone = 'UTC'

app.conf.enable_utc = True
app.conf.beat_schedule = {
    # 'add-every-day-seconds': {
    #     'task': 'core.tasks.get_crypto_info_by_id',
    #     'schedule': 86400,
    # },
    'my-periodic-task': {
        'task': 'core.tasks.clear_today_votes',
        # 'schedule': crontab(hour=0,
        #                     minute=0)
        'schedule': 1,
    },
   # 'add-every-9-min': {
  #      'task': 'core.tasks.change_price_coin',
   #     'schedule': 9 * 60,
   # }
}
