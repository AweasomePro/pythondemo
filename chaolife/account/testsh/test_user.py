from django.test import TestCase
from account.models import User

class TestUserCreate(TestCase):
    user = User()
    # user.name = 'testname'
    user.phone_number = '15726814574'
    user.sex = 1
    user.save()
    User().objects.set_user_is_customer()