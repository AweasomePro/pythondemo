# -*- coding:utf-8 -*-
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
from Crypto.Hash import SHA

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.PublicKey import RSA
from base64 import urlsafe_b64encode
from django.utils.encoding import smart_str
from urllib.parse import quote

import base64
import os
BASE_DIR = os.path.dirname(__file__)



def sign(data):

    with open(BASE_DIR+ '/rsa_pkcs8_key.pem') as f:
        priKey = f.read()
        key = RSA.importKey(priKey)
        h = SHA.new(data)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(h)
        return base64.b64encode(signature)

# 得到的是签名之后的结果
"""
encode byte转str
"""
with open(BASE_DIR+ '/str',encoding='utf-8') as f:
    s = f.read()


urlencoderes = sign(bytes(s,encoding='utf-8'))
print(urlencoderes)
print('第二次,得到了对应的字符')
str2 = str(urlencoderes,encoding='utf-8')
b64strres = quote(str2)
print(str2)
print(str(b64strres))
print('做url safe decode')
print('输出最终结果')

# print(str(b64str,encoding='utf-8'))


# print(str(bytes_res,encoding='utf-8'))

# 接下来需要做urlencode
# from urllib.parse import quote
# print('pre')
# print(quote(str(sign(b'100'))))
#
# '''*RSA验签
# * data待签名数据
# * signature需要验签的签名
# * 验签用支付宝公钥
# * return 验签是否通过 bool值
# '''
def verify(data, signature):
    with open('rsa_public_key.pem') as f:
        pubKey = f.read()
        key = RSA.importKey(pubKey)
        h = SHA.new(data)
        verifier = PKCS1_v1_5.new(key)
        if verifier.verify(h, base64.b64decode(signature)):
            return True
        return False