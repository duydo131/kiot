from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
app = Celery("eureka")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Ho_Chi_Minh'
app.conf.broker_transport_options = {'visibility_timeout': 3600 * 24}

app.conf.beat_schedule = {
    "daily_remove_terminal_fail": {
        "task": "apps.terminals.tasks.process_remove_new_terminal_fail",
        "schedule": crontab(minute=0, hour=0)  # every day
    },
    "daily_restore_when_extend_terminal_fail": {
        "task": "apps.terminals.tasks.process_restore_when_extend_terminal_fail",
        "schedule": crontab(minute=0, hour=0)  # every day
    },
    "daily_open_sell_in_terminal": {
        "task": "apps.terminals.tasks.process_open_sell_in_terminal",
        "schedule": crontab(minute=0, hour=0)  # every day
    },
    "daily_close_sell_in_terminal": {
        "task": "apps.terminals.tasks.process_close_sell_in_terminal",
        "schedule": crontab(minute=0, hour=0)  # every day
    },
    "daily_remove_order_not_success": {
        "task": "apps.terminals.tasks.process_remove_order_not_success",
        "schedule": crontab(minute=0, hour=0)  # every day
    },
}
