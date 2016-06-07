from ..models import Member


def phoneNumberisExist(phoneNumber):
    if Member.objects.filter(phoneNumber = phoneNumber).exists():
        return True
    else:
        return False