# -*- coding:utf-8 -*-
"""hotelBookingProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include,patterns
from django.contrib import admin
from django.conf import settings
urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('chaolifeWeb.urls')),
    url(r'^api/', include('chaolifeWeb.urls')),
    url(r'', include('account.urls')),  # todo 用user做前缀是否更好
    url(r'api/', include('account.urls')), #todo 用user做前缀是否更好
    url(r'^pay/', include('pay.urls')),
    url(r'^api/pay/',include('pay.urls')),
    url(r'', include('chaolife.urls')),
    url(r'api/', include('chaolife.urls')),
    url(r'^hooks/', include('git_hook.urls')),

    url(r'^api/hooks/',include('git_hook.urls')),
    url(r'api/',include('order.urls')),
    url(r'', include('order.urls')),

    url(r'', include('sms.urls')),
    url(r'api/',include('sms.urls')),

    url(r'api/',include('devutils.urls'))
    ]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/',include(debug_toolbar.urls)))

