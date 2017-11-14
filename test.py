import socket
import struct
sock=socket.socket()
sock.bind(("127.0.0.1",9090))
sock.listen(100)
print("bind well")
while True:
    client,clientadd=sock.accept()
    infos=client.recv(1024)
    print(infos)
    port=struct.unpack("!H",infos[2:4])[0]
    ip=struct.unpack("!I",infos[4:8])[0]
    dstport=port
    dstip=socket.inet_ntoa(struct.pack('I',socket.htonl(ip)))
    print(dstip,dstport)
    dstsock=socket.socket()
    dstsock.connect((dstip,dstport))
    client.send(b'\x00\x5a'+infos[2:8])
    while True:
        try:

            info=client.recv(1024)
            print("recv from ie")
            print(info)
            dstsock.send(info)
            print("send to host.")
            dstrecv=dstsock.recv(1024)
            print("recv from host")
            print(dstrecv)
            client.send(dstrecv)
            print("send to ie.")
        except:
            break
    client.close()

