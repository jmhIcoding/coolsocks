__author__ = 'jmh081701'
from crypto.rc4 import rc4
import socket
prepwd="uestc"
hellopkt="uestchello"
maxclient=100
serverip="127.0.0.1"
serverport=9091
sock=socket.socket()
sock.bind((serverip,serverport))
sock.listen(maxclient)
while True:
    client,clientaddr=sock.accept()
    hello=client.recv(1024)
    if hello==rc4(prepwd,hellopkt):
        client.send(bytes("good!!",'utf8'))
        client.close()
    else:
        client.send(bytes("error!!",'utf8'))
        client.close()