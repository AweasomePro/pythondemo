import unittest

from hotelBooking import Hotel
from django.db.models import Count,Min,Max

class HotelFilterTest(unittest.TestCase):
    def testFilter(self):
        hotels = Hotel.objects.annotate(

        )