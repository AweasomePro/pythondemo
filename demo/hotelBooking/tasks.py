from celery.task import task
import time

@task
def add(a,b):
    print('start')
    time.sleep(5)
    print('success')
    return a+b