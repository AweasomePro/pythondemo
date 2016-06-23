from Crypto.PublicKey import RSA
import os

print()
print(os.path.join('../rsa_public_key.pem'))
# publickey = RSA.importKey(open(os.path.join(r'../rsa_public_key.pem','r')).read())
# privatekey=RSA.importKey(open(r'../pkcs8_rsa_private_key.pem','r').read())
# print(os.path.abspath(os.path.join('../rsa_publick_key.pem', os.pardir, os.pardir)))