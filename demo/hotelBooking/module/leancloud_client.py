import json

import requests
from rest_framework.response import Response

APP_ID = None
APP_KEY = None
MASTER_KEY = None


REGION = 'CN'
USE_HTTPS = True
SERVER_VERSION = '1.1'
host = 'api.leancloud.cn'

TIMEOUT_SECONDS = 15


def init(app_id,app_key=None,master_key = None):
    if (not app_key) and (not master_key):
        raise RuntimeError('app_key or master_key must specified')
    global APP_ID, APP_KEY, MASTER_KEY
    APP_ID = app_id
    APP_KEY = app_key
    MASTER_KEY = master_key

def need_init(func):
    def new_func(*args,**kwargs):
        if APP_ID is None:
            raise RuntimeError('LeanCloud APP_ID must be initialized')
        headers = {
            'X-LC-Id': APP_ID,
            'X-LC-Key': APP_KEY,
            'Content-Type': 'application/json'
        }
        return func(headers=headers,*args,**kwargs)
    return new_func

def get_base_url():
    r = {
        'schema': 'https' if USE_HTTPS else 'http',
        'version': SERVER_VERSION,
        'host': host,
    }
    return '{schema}://{host}/{version}'.format(**r)

@need_init
def post(url,params,headers=None):
    response = requests.post(get_base_url()+url,headers = headers,data=json.dumps(params,separators=(',',':')),timeout = TIMEOUT_SECONDS)
    print(json.dumps(params,separators=(',',':')))
    print(headers)
    print(get_base_url()+url)
    response.encoding = 'utf-8'
    # 使用异步
    print(response.content)
    print(response.status_code)
    print(type(response.json()))
    return response
