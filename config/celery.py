from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
app = Celery("eureka")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Ho_Chi_Minh'
app.conf.broker_transport_options = {'visibility_timeout': 3600 * 24}

app.conf.beat_schedule = {
}
