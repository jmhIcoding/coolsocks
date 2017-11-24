__author__ = 'jmh081701'
import struct

def str2bytes(_str):
    rst=b''
    for i in range(len(_str)):
        rst+=struct.pack('!B',ord(_str[i]))
    return rst
def bytes2str(_bytes):
    _str=''
    for i in  range(len(_bytes)):
        _str+=chr(_bytes[i])
    return  _str
def test_str2byte():
    if bytes2str(str2bytes("hello"))!="hello":
        print("Detect str2bytes Function Error.")
        exit(-1)
    print("str2byte Function well")
if __name__ == '__main__':
    test_str2byte()