from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# app = Celery('caught_fish',
#             broker='transport://chu:ehddnjs369!@localhost:port//',
#             backend='db+sqlite:///results.sqlite',
#             include=['caught_fish.tasks'])

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('caught_fish')
app.config_from_object('django.conf:settings', namespace='CELERY')

#등록된 장고 앱 설정에서 task 불러오기
app.autodiscover_tasks()