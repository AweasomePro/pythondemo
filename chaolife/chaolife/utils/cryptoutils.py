# -*- coding: utf-8 -*-
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import hashlib
import base64
import os
dsize = SHA.digest_size
sentinel = Random.new().read(15 + dsize)
BASE_DIR = os.path.dirname(__file__)

rsa_private_key_pkcs8 = RSA.importKey(open(BASE_DIR + '/rsa_private_key_pkcs8.pem').read())
rsa_public_key = RSA.importKey(open(BASE_DIR + '/rsa_public_key.pem').read())


def sign_pkcs8(data):
    signer = Signature_pkcs1_v1_5.new(rsa_private_key_pkcs8)
    digest = SHA.new()
    digest.update(data.encode(encoding='utf-8'))
    signature = signer.sign(digest)
    return base64.b64encode(signature)


def sign(data):
    with open(BASE_DIR + '/rsa_private_key_pkcs8.pem') as f:
        priKey = f.read()
        key = RSA.importKey(priKey)
        h = SHA.new(data)
        signer = Signature_pkcs1_v1_5.new(key)
        signature = signer.sign(h)
        return base64.b64encode(signature)


        # '''*RSA验签
        # * data待签名数据
        # * signature需要验签的签名
        # * 验签用支付宝公钥
        # * return 验签是否通过 bool值
        # '''


def verify_pkcs8(data, signature):
    with open(BASE_DIR + '/pkcs8_rsa_private_key.pem') as f:
        pubKey = f.read()
        key = RSA.importKey(pubKey)
        h = SHA.new(data)
        verifier = Signature_pkcs1_v1_5.new(key)
        if verifier.verify(h, base64.b64decode(signature)):
            print('验证成功')
            return True
        print("验证错误")
        return False


def verify(data, signature):
    with open(BASE_DIR + '/rsa_private_key.pem') as f:
        pubKey = f.read()
        key = RSA.importKey(pubKey)
        h = SHA.new(data)
        verifier = Signature_pkcs1_v1_5.new(key)
        if verifier.verify(h, base64.b64decode(signature)):
            print('验证成功')
            return True
        print("验证错误")
        return False


def rsa_base64_encrypt(data):
    cipher = Cipher_pkcs1_v1_5.new(rsa_public_key)
    cipher_text = base64.b64encode(cipher.encrypt(data))
    print('加密后' + str(cipher_text, encoding='utf-8'))
    return cipher_text


def rsa_decrypt(message):
    cipher = Cipher_pkcs1_v1_5.new(rsa_private_key_pkcs8)
    return str(cipher.decrypt(base64.b64decode(message), sentinel), encoding='utf-8')


if __name__ == '__main__':
    print(hashlib.md5(bytes('123456', encoding='utf-8')).hexdigest())
    print(
        rsa_base64_encrypt(
            bytes(
                hashlib.md5(bytes('123456', encoding='utf-8')).hexdigest(), encoding='utf-8'
            )
        )
    )
    print(rsa_decrypt(
        'p6SVxmsl4OrNVdH+Ko8f7u7AFMO++FxIG70u3ZooDm20b5Zljf0LGM4iDlZIja7N/sxCxMhIWNZCVSdMWR4nhUqGpeiiySuME6jS0n44h/Du+MLppUqXKlk63GDkNW0P0zlt9S2T2FYgq/diDF/LadcbqRz9Leyi2cE0Gjvj6Gg='))
