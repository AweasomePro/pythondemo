# from Crypto.PublicKey import RSA
# from Crypto.Hash import SHA256
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP
# import os
# print(os.path.dirname(os.path.abspath(__file__)))
# rsa_public_key = RSA.importKey(open(os.path.dirname(os.path.abspath(__file__))+r'\rsa_public_key.pem','r').read())
# rsa_private_key = RSA.importKey(open(os.path.dirname(os.path.abspath(__file__))+r'\rsa_private_key.pem','r').read())
# print(rsa_private_key)
# print(rsa_public_key)
# key = RSA.generate(1024)
# pubkey = key.publickey().key
#
#
#
# def Decrypt(prikey, data):
#     cipher = PKCS1_OAEP.new(prikey, hashAlgo=SHA256)
#     return cipher.decrypt(data)
#
#
#
# def Encrypt(pubkey, data):
#     try:
#         cipher = PKCS1_OAEP.new(pubkey, hashAlgo=SHA256)
#         return cipher.encrypt(data)
#     except:
#         # traceback.print_exc()
#         return None

# print(Decrypt(key,'hahahadf'))