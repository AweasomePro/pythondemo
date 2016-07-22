# from hotelBooking.core.utils.serializer_helpers import wrapper_response_dict
# from hotelBooking.models.image import HotelImg,RoomImg
# from hotelBooking.models.usermodels import User
# __all__ = [
#     "User",
#     "CustomerMember",
#     "FranchiseeMember"
#     "City",
#     "Province",
#     "Hotel",
#     "Room",
#     "RoomImg",
#     "HotelImg",
#     "Installation",
#     "Order",
#     "Product",
#     "RoomPackage",
#     "HotelPackageOrderSnapShot",
#     "wrapper_response_dict",
# ]
from django.utils.encoding import smart_str
from hotelBooking.tasks import checkHousePackageState

default_app_config = 'hotelBooking.apps.HotelbookingConfig'
