__author__ = 'jmh081701'
#coding:utf8
import sys
sys.path.append("/home/coolsocks/")
import struct
from crypto.hash import  hashkey
from crypto.basetool import str2bytes
from  crypto.basetool import bytes2str

import  threading

lock=threading.Semaphore(1)

def rc4(_prepwd,_cipher,iKeyLen=None):
    '''
    :param _prepwd: 预主密钥
    :param _cipher: 密文或者明文
    :param iKeyLen: 密钥长度
    :return:
    '''
    #lock.acquire()
    if type(_prepwd)==type("abcd"):
        _prepwd=hashkey(_prepwd)
    if type(_cipher)==type("abcd"):
        _cipher=str2bytes(_cipher)
    _prepwd=struct.pack("!H",_prepwd)
    if iKeyLen==None:
        iKeyLen=len(_prepwd)
    Sbox=[]
    Key=[]
    for i in range(256):
        Sbox.append(i)
        Key.append(0)
    for i in range(1):
        Sbox[i]=128

    k=0
    for i in range(256):
        Key[i]=_prepwd[k]
        k=(k+1)%iKeyLen
        Sbox[0]=(Sbox[0]*11+Key[i])%256
    '''
    j=0
    for i in  range(256):
        j=(j+Sbox[i]+Key[i])%256
        tmp=Sbox[i]
        Sbox[i]=Sbox[j]
        Sbox[j]=tmp
    '''

    '''
    加密
    '''
    rst=b''
    j=0
    i=0
    cil=len(_cipher)
    while True:
        #print(i,len(_cipher))
        if i>=len(_cipher):
            break
        if i < cil:
            _new=_cipher[i]^Sbox[0]
        else:
            rst+=_cipher[cil:]
            break
            _new=_cipher[i]
        _new=struct.pack("!B",_new)
        rst+=_new
        i=i+1
    #lock.release()
    return rst
def test_rc4():
    plaintext=b"\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6\x01\x02\xea\xb6\xea\xb6"
    plaintext+=plaintext
    plaintext+=plaintext
    plaintext+=plaintext
    plaintext+=plaintext
    print(rc4("abcdegefdfd",plaintext))
    print(len(plaintext))
    if rc4("abcdegefdfd",rc4("abcdegefdfd",plaintext))!=plaintext:
        print("Detect rc4 Function Error.")
        exit(-1)
    print("rc4 Function well.")

if __name__ == '__main__':
    test_rc4()

