from datetime import datetime
from datetime import timedelta
def validate_book_date(checkinDate,checkoutDate):
    delta_days = checkoutDate - checkinDate
    return  delta_days.days >= 1
