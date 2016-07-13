import pymysql
pymysql.install_as_MySQLdb()
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

# Configure celery to use the django-celery backend.  fot the databasebackend

# Configure celery to use the django-celery backend.  fot the databasebackend
