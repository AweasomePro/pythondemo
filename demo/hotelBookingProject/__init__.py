import pymysql
pymysql.install_as_MySQLdb()
from .celery import app as celery_app

# Configure celery to use the django-celery backend.  fot the databasebackend
celery_app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)
# Configure celery to use the django-celery backend.  fot the databasebackend
# app.conf.update(
#     CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
# )