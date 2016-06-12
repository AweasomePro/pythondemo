from ..models import Member


def phoneNumberisExist(phoneNumber):
    if Member.objects.get(phoneNumber = phoneNumber).exists():
        return True
    else:
        return False