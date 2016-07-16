from django.test import TestCase
from hotelBooking import Hotel,Room,RoomPackage


class housepackageTestCase(TestCase):
    def setUp(self):
        pass

    def test_housepackage_can_create(self):
        for housepackage in RoomPackage.objects.all().iterator():
            print(housepackage)

