import json
import requests
from . import settings
from .settings import PUSH_CLIENT_SETTINGS,PUSH_PARTNER_SETTINGS
"""
与Leancloud通信的Client
"""

# 注意 channel名称只能包含 字母和数字
channel_customer = 'customer'
channel_hotel_partner = 'Hpartner'

def push_init(func):
    """
    为push方法添加所必要的 key
    :param func:
    :return:
    """
    def new_func(*args,**kwargs):
        if settings.APP_ID is None:
            raise RuntimeError('LeanCloud APP_ID must be initialized')
        headers = {
            'X-LC-Id': PUSH_CLIENT_SETTINGS.get('APP_ID'),
            'X-LC-Key': PUSH_CLIENT_SETTINGS.get('APP_KEY'),
            'Content-Type': 'application/json'
        }
        return func(headers=headers,*args,**kwargs)
    return new_func


def push_init_with_setting(push_settings):
    def decorator(func):
        def wrapper(*args,**kwargs):
            if settings.APP_ID is None:
                raise RuntimeError('LeanCloud APP_ID must be initialized')
            headers = {
                'X-LC-Id': push_settings.get('APP_ID'),
                'X-LC-Key': push_settings.get('APP_KEY'),
                'Content-Type': 'application/json'
            }
            return func(headers= headers,*args,**kwargs)
        return wrapper
    return decorator


def get_base_url():
    r = {
        'schema': 'https' if settings.USE_HTTPS else 'http',
        'version': settings.SERVER_VERSION,
        'host': settings.host,
    }
    return '{schema}://{host}/{version}'.format(**r)

@push_init
def post(url,params,headers=None):
    """
    post 请求 leancloud接口的封装函数
    :param url: 将需要的业务url拼接在leancloud域名之后
    :param params: 传递的参数
    :param headers: 调用需要的凭证封装在了header中
    :return:
    """
    response = requests.post(get_base_url() + url, headers=headers, data=json.dumps(params, separators=(',', ':')),
                             timeout=settings.TIMEOUT_SECONDS)
    response.encoding = 'utf-8'
    return response


def _post(url,params,headers=None):
    response = requests.post(get_base_url() + url, headers=headers, data=json.dumps(params, separators=(',', ':')),
                             timeout=settings.TIMEOUT_SECONDS)
    response.encoding = 'utf-8'
    return response


@push_init_with_setting(PUSH_PARTNER_SETTINGS)
def post_to_business(url,params,headers=None):
    response = requests.post(get_base_url() + url, headers=headers, data=json.dumps(params, separators=(',', ':')),
                             timeout=settings.TIMEOUT_SECONDS)
    response.encoding = 'utf-8'
    return response


@push_init_with_setting(PUSH_CLIENT_SETTINGS)
def post_to_client(url,params,headers=None):
    _post(url,params,headers)
