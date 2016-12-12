#!/usr/bin/env python

from Crypto.Cipher import DES
import sys
import base64

global key
global iv

'''
        0x12t
        0x34t
        0x56t
        0x78t
        -0x70t
        -0x55t
        -0x33t
        -0x11t
'''
key = b'\xe0\xad\x10\x0b\x10\x76\x3b\x76'
iv = b'\x12\x34\x56\x78\x90\xab\xcd\xef'


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


def decrypt(deskey, ciper, base64=True):
    try:
        decryptText = decode_base64(ciper) if base64 is True else ciper.decode('hex')
        cipherX = DES.new(deskey, DES.MODE_CBC, iv)
        y = cipherX.decrypt(decryptText)
        print y[0: ord(y[len(y) - 1]) * -1]
    except:
        print "Error"


def encrypt(deskey, plain, base64=True):
    try:
        if plain is not '':
            plen = len(plain) % 16
        if plen != 0:
            padding = 16 - plen
            plain += chr(padding) * padding
        cipherX = DES.new(deskey, DES.MODE_CBC, iv)
        print cipherX.encrypt(plain).encode('base64')
    except:
        print "Error"


if __name__ == '__main__':
    try:
        if sys.argv[1] == '-d':
            decrypt(key, sys.argv[2], '-b' in sys.argv)
        elif sys.argv[1] == '-e':
            encrypt(key, sys.argv[2])
    except IndexError:
        print '''
Decrypt DES - v0.1
Code by Jielei@4dogs.cn

Usage:
  Decrypt: %s -d BASE64_Encoded_Ciper [-b: Base64 encode]
  Encrypt: %s -e Plain
''' % (sys.argv[0], sys.argv[0])
    except Exception as e:
        print str(e)
