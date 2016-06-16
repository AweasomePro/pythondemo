from django.test import TestCase
from hotelBooking.models import User

class ModelTestCase(TestCase):
    def setUp(self):
        pass
    def testMemberIsExist(self):
        self.assertEquals(True,User.objects.filter(phoneNumber=15726814574).exists())