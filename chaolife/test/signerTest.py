from datetime import timedelta



from django.core.signing import TimestampSigner
from django.core.signing import Signer
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
message = '100'
text = ""
random_generator = Random.new().read

PADDING = '{'

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (16 - len(s) % 16) * PADDING
# with open('rsa_public_key.pem') as f:
#     key = f.read()
#     rsakey = RSA.importKey(key)
#     print(rsakey)
#
#     cipher = Cipher_pkcs1_v1_5.new(rsakey)
#     cipher_text = base64.b64encode(cipher.encrypt(bytes(message,encoding='utf-8')))
#     print(cipher_text)
#
# with open('rsa_private_key.pem') as f:
#     key = f.read()
#     rsakey2 = RSA.importKey(key)
#     print(rsakey2)
#     cipher2 = Cipher_pkcs1_v1_5.new(rsakey2)
#     text2 =cipher2.decrypt(base64.b64decode(cipher_text), random_generator)

def sign(data):
    with open('pkcs8_rsa_private_key.pem') as f:
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
res = sign(b'100')
print(res)
if verify(b'100',res):
    print('success')
else:
    print('faield')
#

# raw_data = 'partner="2088701924089318"&seller="774653@qq.com"&out_trade_no="123000"&subject="123456"&body="2010新款NIKE 耐克902第三代板鞋 耐克男女鞋 386201 白红"&total_fee="0.01"¬ify_url="http://notify.java.jpxx.org/index.jsp"'
# # sign_data = sign(raw_data)
# # print("sign_data: ", sign_data )
# # print(verify(raw_data, sign_data))
#
# key = RSA.generate(2048)
#
# binPrivKey = key.exportKey('DER')
# binPubKey =  key.publickey().exportKey('DER')
#
# privKeyObj = RSA.importKey(binPrivKey)
# pubKeyObj =  RSA.importKey(binPubKey)
#
# msg = "attack at dawn"
# emsg = pubKeyObj.encrypt(msg, 'x')[0]
# dmsg = privKeyObj.decrypt(emsg)
#
# assert(msg == dmsg)



