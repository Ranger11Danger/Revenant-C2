import hashlib
import random
import base64
from Crypto.Cipher import AES
from Crypto import Random
import nacl.secret
import nacl.utils
class key:
    
    def __init__(self):
        self.p = 991
        self.g = 6
        self.secret = random.randint(1,10)
        self.half_key = self.gen_half()

    def gen_half(self):
        half_key = pow(self.g, self.secret, self.p)
        return half_key

    def gen_full(self, new_half):
        full_key = pow(new_half, self.secret, self.p)
        return hashlib.sha256(str(full_key).encode()).hexdigest()[:32].encode()

class C2_AES:
    
    def __init__(self, key):
        self.box = nacl.secret.SecretBox(key)

    def encrypt(self, raw):
        msg = self.box.encrypt(raw.encode())
        #msg = base64.b64encode(msg)
        #print(len(msg))
        return(msg)

    def decrypt(self, enc):
        #enc = base64.b64decode(enc)
        msg = self.box.decrypt(enc)
        return msg