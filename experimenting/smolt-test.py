import base64
import hashlib
import hmac
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

# We are trying to:encode an outgoing Salmon message.

marnanel_salmon_link = 'https://anticapitalist.party/api/salmon/65294'

attempting_mention = """<entry xmlns='http://www.w3.org/2005/Atom'>
  <id>tag:marnanel.org,idk</id>
  <author><name>marnanel@marnanel.org</name><uri>marnanel@marnanel.org</uri></author>
  <link rel="mentioned" href="acct:marnanel@anticapitalist.party" />
  <content>@marnanel@anticapitalist.party Hello. This shows that the Salmon library is working.</content>
  <updated>2009-12-18T20:04:03Z</updated>
</entry>
"""

secret_key = b'\xbf\xe7drAw\x1ce\xba=`\x0e\xb2<\xf3\xa6\xa0`\x16\x9d\xe5\x93\xe7\x9b\xderj\xda%\xf6\x1f\x9c\xb8*\xc7\x89\xa0\xa2\x00\xd9g\xb0\xaf\xd3\x8c[\xe4\xaef#\x8a\x8c&\xb5>w\xdd66\xacWI\x14\xb1\xf3o/\x99\xfd\xbd7x\xf3\xc1\xab !k\xa9\xb2\xfd"E\xe2m/\x0c\xcf\x03\x8d\x1f\x92\xbd%\xf7\xa8\xbf4\xd85\xa9[\x0f\x92%\x150V)i\xea\xd0\xae\x9fDt\x8c]\xba\xf4\xaa\x02\xc7\x12\x92\xefS}'

def base64url_encode(data):
    """
    base64-encodes its input, using the modified URL-safe
    alphabet given in RFC 4648.
    """
    return str(base64.b64encode(bytes(data, encoding='UTF-8'),
        altchars=b'-_'),
            encoding="ASCII")

def base64url_decode(data):
    """
    base64-decodes its input, using the modified URL-safe
    alphabet given in RFC 4648.
    """
    return base64.b64decode(bytes(data, encoding='ASCII'),
            altchars='-_')

def make_envelope(data, secret_key, key_id=None):
    # XXX do this with a proper XML producer
    # XXX none of the strings are escaped properly

    signature = hmac.new(
            key = secret_key,
            msg = bytes(data, encoding='UTF-8'),
            digestmod = hashlib.sha256).hexdigest()

    result = """<?xml version='1.0' encoding='UTF-8'?>
<me:env xmlns:me='http://salmon-protocol.org/ns/magic-env'>
  <me:data type='application/atom+xml'>
"""

    result += base64url_encode(data)

    result += """
  </me:data>
  <me:encoding>base64url</me:encoding>
  <me:alg>RSA-SHA256</me:alg>"""

    if key_id is not None:
        result += '<me:sig key_id="%s">\n' % (key_id,)
    else:
        result += '<me:sig>\n'

    result += base64url_encode(signature)

    result += """
  </me:sig>
</me:env>"""

    return result

def whatsit():
    # XXX what?!
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)

def main():
    print(make_envelope(data=attempting_mention, secret_key=secret_key))

if __name__=='__main__':
    main()

