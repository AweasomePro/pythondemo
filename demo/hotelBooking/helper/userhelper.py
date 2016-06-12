from ..models import Member
from django.core.exceptions import ObjectDoesNotExist


def phoneNumberExist(phoneNumber):
    try:
        Member.objects.get(phoneNumber=phoneNumber)
        return True
    except ObjectDoesNotExist:
        return False
