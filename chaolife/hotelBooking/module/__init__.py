from . import leancloud_client
from hotelBooking import Mysettings as settings
leancloud_client.init(app_key=settings.APP_KEY,app_id=settings.APP_ID,master_key=settings.MASTER_KEY)