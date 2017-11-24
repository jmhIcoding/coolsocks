__author__ = 'jmh081701'
_mod=65521
_p=1999
def hashkey(key):
    rst=1
    for i in range(len(key)):
        rst=(rst*_p% _mod +ord(key[i]))%_mod
    return  int(rst)
def test_hashkey():
    if hashkey("abcd")!=252380003:
        print("Detect hashkey Function ERROR.")
        exit(-1)
    else:
        print("hashkey Function well.")
if __name__ == '__main__':
    test_hashkey()