from django.utils.encoding import force_text, python_2_unicode_compatible
from hotelBooking.core.models._base import BaseModel
from hotelBooking.models import User,UserManager
class Meta:
    app_label = 'hotelBooking'
__all__ = ["python_2_unicode_compatible",
           "BaseModel",
           "User"
           ]