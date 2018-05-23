#!/usr/bin/python

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from struct import pack
import base64
import hashlib

FILENAME = 'test-key.rsa'

# XXX duplicated
def base64url_encode(data):
    """
    base64-encodes its input, using the modified URL-safe
    alphabet given in RFC 4648.
    """
    b = base64.b64encode(s=data,
            altchars=b'-_')
    return str(b, encoding='ASCII')

def base64url_decode(data):
    """
    base64-decodes its input, using the modified URL-safe
    alphabet given in RFC 4648.
    """
    return base64.b64decode(bytes(data, encoding='ASCII'),
            altchars='-_')

def bignum_to_bytes(bignum):

    temp = bignum
    result = []

    while temp!=0:
        result.append(temp & 0xFF)
        temp >>= 8

    result.reverse()
    return bytes(result)

key = RSA.generate(1024, progress_func=print)

print(key)

expo1 = ((key.d)%((key.p)-1))
expo2 = ((key.d)%((key.q)-1))

print('Modulus: ',str(key.n))
print('Public exp: ',str(key.e))
print('Private exp: ',str(key.d))

print('Magic signature: RSA.{0}.{1}'.format(
    base64url_encode(bignum_to_bytes(key.n)),
    base64url_encode(bignum_to_bytes(key.e)),
    ))

f = open(FILENAME, 'wb')
f.write(key.exportKey('PEM'))
f.close()
print('Key written to '+FILENAME+'.')

