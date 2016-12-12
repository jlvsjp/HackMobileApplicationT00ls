#!/usr/bin/env python
from Crypto.Cipher import AES
import sys
import base64

global key

# key = b'\x38\xF7\xFC\x25\x94\x81\x1D\xD5\x0D\x69\x30\x05\x49\x45\xDB\xA9'
# key = b'\xeb\x19\x92\x5c\x86\xcd\xf0\x9e\x99\xdc\xfe\x3b\xf7\x9d\x5f\x87\x88\x16\xdc\xdc\x8a\x7e\x9c\x11\xd0\xf5\x10\x5c\x7f\x26\xe3\xfa'
# key = b'\xd7\xf9\xb7\x38\x88\x14\x20\xa6\x83\xf5\x54\x27\x1b\x01\xc4\x58\x5c\x14\x8c\x11\xfa\xfd\x15\xe6\xbe\x01\x5b\x53\x2a\x7a\x85\x3d'

key = b'\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20'


def decode_base64(data):
    """
    Decode base64, padding being optional.
    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.
    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return base64.decodestring(data)


def decrypt(aeskey, ciper, base64=True):
    ciper = decode_base64(ciper) if base64 is True else ciper.decode('hex')
    if ciper is not '':
        obj = AES.new(aeskey, AES.MODE_ECB)
        print obj.decrypt(ciper).strip()
    else:
        print 'Error string!'


def encrypt(aeskey, plain, base64=True):
    if plain is not '':
        plen = len(plain) % 16
        if plen != 0:
            padding = 16 - plen
            plain += chr(padding) * padding
        obj = AES.new(aeskey, AES.MODE_ECB)
        print obj.encrypt(plain).encode('base64')
    else:
        print 'Error string!'


if __name__ == '__main__':
    try:
        if sys.argv[1] == '-d':
            decrypt(key, sys.argv[2], '-b' in sys.argv)
        elif sys.argv[1] == '-e':
            encrypt(key, sys.argv[2])
    except IndexError:
        print '''
Decrypt AES - v0.1
Code by Jielei@4dogs.cn

Usage:
  Decrypt: %s -d BASE64_Encoded_Ciper [-b: Base64 encode]
  Encrypt: %s -e Plain
''' % (sys.argv[0], sys.argv[0])
    except Exception as e:
        print str(e)
