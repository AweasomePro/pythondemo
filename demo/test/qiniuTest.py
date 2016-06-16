import qiniu

QINIU_ACCESS_KEY = 'u-ryAwaQeBx9BS5t8OMSPs6P1Ewoqiu6-ZbbMNYm'
QINIU_SECRET_KEY = 'hVXFHO8GusQduMqLeYXZx_C5_c7D-VSwz6AKhjZJ'
QINIU_BUCKET_DEFAULT = 'hotelbook'

q = qiniu.Auth(QINIU_ACCESS_KEY,QINIU_SECRET_KEY)
key = 'hello'
data = 'hello qiniu!'
token = q.upload_token(QINIU_BUCKET_DEFAULT)
res, info = qiniu.put_data(token,key,data)
if res is not None:
    print('All is Ok')
else:
    print(info)
