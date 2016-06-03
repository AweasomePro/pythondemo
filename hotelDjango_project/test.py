from hotel.models import  Person
from hotelDjango_project import settings
settings.configure()
Person.objects.create(name="zxw",age=24)
Person.objects.get(name="zhuoxiuwu")
