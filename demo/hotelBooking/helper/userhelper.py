from ..models import User
from django.core.exceptions import ObjectDoesNotExist


def phoneNumberExist(phoneNumber):
    try:
        User.objects.get(phone_number=phoneNumber)
        return True
    except ObjectDoesNotExist:
        return False

def updateAvatar(phone_number,avatar_url):
    User.objects.all().filter(phone_number=phone_number).update(avatar =avatar_url)


