#coding:utf-8
import socket
import struct
import  threading
sock=socket.socket()
sock.bind(("127.0.0.1",9090))
sock.listen(100)
print("bind well")
threads=[]
max=1024
sem=threading.Semaphore(max)
def recv_fromie(clientsock,dstsock):
    while True:
        try:
            info =clientsock.recv(1024)
            if len(info)==0:
                clientsock.close()
                sem.release()
                return

            print("recv from ie")
            #print(info)
            dstsock.send(info)
            print("send to host.")
        except:
            sem.release()
            return

def recv_fromhost(client,dstsock):
    while True:
        try:
            dstrecv=dstsock.recv(1024)
            if len(dstrecv)==0:
                dstrecv.close()
                sem.release()
                return
            print("recv from host.")
            #print(dstrecv)
            client.send(dstrecv)
            print("send to ie.")
        except:
            sem.release()
            return
def loop(client):
    try:
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
        #while True:
        #    try:
        '''
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
        '''

        th =threading.Thread(target=recv_fromie,args=[client,dstsock])
        sem.acquire()
        th.start()
        th2 =threading.Thread(target=recv_fromhost,args=[client,dstsock])
        sem.acquire()
        th2.start()
        threads.append(th)
        threads.append(th2)
            #except:
            #    break
        #client.close()
    except:
        pass

while True:
    client,clientadd=sock.accept()
    th =threading.Thread(target=loop,args=[client])
    th.start()
    threads.append(th)
for each in threads:
    each.join()


