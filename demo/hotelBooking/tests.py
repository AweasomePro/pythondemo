from django.test import TestCase
from hotelBooking.models import Member

class ModelTestCase(TestCase):
    def setUp(self):
        pass
    def testMemberIsExist(self):
        self.assertEquals(True,Member.objects.filter(phoneNumber=15726814574).exists())