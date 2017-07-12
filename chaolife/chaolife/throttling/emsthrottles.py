#-*- coding: utf-8 -*-
from rest_framework.throttling import BaseThrottle,AnonRateThrottle,UserRateThrottle

class RegistrationEmsThrottle(AnonRateThrottle):
    scope = 'registrationEmsThrottle'

