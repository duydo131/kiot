#!/bin/bash
ddd

nohup celery -A config worker -B -l info -c 3 &
python manage.py runserver 0.0.0.0:8000