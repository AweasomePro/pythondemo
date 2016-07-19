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
import base64
import os
BASE_DIR = os.path.dirname(__file__)



def sign(data):

    with open(BASE_DIR+ '/rsa_private_key.pem') as f:
        priKey = f.read()
        key = RSA.importKey(priKey)
        h = SHA.new(data)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(h)
        return base64.b64encode(signature)
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