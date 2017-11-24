__author__ = 'jmh081701'
from crypto.rc4 import  rc4
import socket
prepwd="uestc"
hellopkt="uestchello"
serverip="127.0.0.1"
serverport=9091
client=socket.socket()
client.connect((serverip,serverport))
client.send(rc4(prepwd,hellopkt))
info=client.recv(1024)
print(info)
