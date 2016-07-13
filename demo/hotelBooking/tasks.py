# encoding:utf-8
from celery.task import task
from hotelBookingProject.celery import app
from hotelBooking.models import User
from hotelBooking.module import push

@task
def notify(phone_number, message):
    user = User.objects.get(phone_number=phone_number)
    installations = user.installation_set.filter(active=True).all()
    for installation in installations:
        push.send(
            where= {'installationId':str(installation.installationId)},
            data={'alert':message}
        )
