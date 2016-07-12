# encoding:utf-8
from celery.task import task
import time

@task
def _do_kground_work (name ):
    for i in range(1, 10):
        print('hello:%s %s' % (name, i))
        time.sleep(1)