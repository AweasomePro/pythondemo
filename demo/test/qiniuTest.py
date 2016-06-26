import qiniu
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

QINIU_ACCESS_KEY = 'u-ryAwaQeBx9BS5t8OMSPs6P1Ewoqiu6-ZbbMNYm'
QINIU_SECRET_KEY = 'hVXFHO8GusQduMqLeYXZx_C5_c7D-VSwz6AKhjZJ'
QINIU_BUCKET_DEFAULT = 'hotelbook'

#构建鉴权对象
q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)

#要上传的空间
bucket_name = 'hotelbook'

#上传到七牛后保存的文件名
key = 'my-python-logo.png';

policy = {
    'callbackUrl': 'agesd.com/avatar/upload/callback',
    'callbackBody': 'filename=$(fname)&filesize=$(fsize)'
}
#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600,policy)

#要上传文件的本地路径
localfile = 'shanghai.jpg'

ret, info = put_file(token, key, localfile)
print(ret)
print(info)
