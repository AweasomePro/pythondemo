from ..models import User
from django.core.exceptions import ObjectDoesNotExist


def phoneNumberExist(phoneNumber):
    try:
        User.objects.get(phone_number=phoneNumber)
        return True
    except ObjectDoesNotExist:
        return False

def updateAvatar(userId,avatar_url):
    User.objects.all().filter(id=userId).update(avatar =avatar_url)


