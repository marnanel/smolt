import base64
import hashlib
import hmac
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# We are trying to:encode an outgoing Salmon message.

marnanel_salmon_link = 'https://anticapitalist.party/api/salmon/65294'

attempting_mention = """<entry xmlns='http://www.w3.org/2005/Atom'>
  <id>tag:marnanel.org,idk,2</id>
  <author><name>test@marnanel.org</name><uri>test@marnanel.org</uri></author>
  <link rel="mentioned" href="acct:marnanel@anticapitalist.party" />
  <content>@marnanel@anticapitalist.party Hello. This shows that the Salmon library is working.</content>
  <updated>2009-12-18T20:04:03Z</updated>
</entry>
"""

def base64url_encode(data):
    """
    base64-encodes its input, using the modified URL-safe
    alphabet given in RFC 4648.
    """
    return str(base64.b64encode(data,
        altchars=b'-_'),
            encoding="ASCII").replace('=','')

def base64url_encode_str(s):
    return base64url_encode(bytes(s, encoding='ASCII'))

def make_envelope(data, secret_key, key_id=None):

    signature_base_string = '.'.join([
            base64url_encode_str(data),
            base64url_encode_str('application/atom+xml'),
            base64url_encode_str('base64url'),
            base64url_encode_str('RSA-SHA256'),
            ])

    h = SHA256.new(bytes(signature_base_string, encoding='ASCII'))

    signer = PKCS1_v1_5.new(key = secret_key)

    signature = signer.sign(h)

    b64_signature = str(base64.b64encode(signature,
        altchars=b'-_'),
            encoding="ASCII")

    result = """<?xml version='1.0' encoding='UTF-8'?>
<me:env xmlns:me='http://salmon-protocol.org/ns/magic-env'>
  <me:data type='application/atom+xml'>
"""

    result += base64url_encode_str(data)

    result += """
  </me:data>
  <me:encoding>base64url</me:encoding>
  <me:alg>RSA-SHA256</me:alg>"""

    if key_id is not None:
        result += '<me:sig key_id="%s">\n' % (key_id,)
    else:
        result += '<me:sig>\n'

    result += b64_signature

    result += """
  </me:sig>
</me:env>"""

    return result

def main():
    key = RSA.importKey(open('test-key.rsa', 'rb').read())
    print(make_envelope(data=attempting_mention, secret_key=key))

if __name__=='__main__':
    main()

