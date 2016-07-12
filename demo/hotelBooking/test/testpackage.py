from django.test import TestCase
from hotelBooking import Hotel,House,HousePackage


class housepackageTestCase(TestCase):
    def setUp(self):
        pass

    def test_housepackage_can_create(self):
        for housepackage in HousePackage.objects.all().iterator():
            print(housepackage)

