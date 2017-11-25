#coding:utf8
__author__ = 'jmh081701'
import sys
sys.path.append("/home/coolsocks")
from crypto.rc4 import  rc4
import socket
import  define
import  config
import  threading
import  struct
configs=config.get_config("ssever.json")

class server:
    def __init__(self,configs):
        if (configs["type"]!="server"):
            print("Please check the configure file,make sure it 's for server.")
            exit(-1)
        self.prepwd=configs["password"]
        self.hellopkt=configs["hello"]
        self.serverip=configs["server_ip"]
        self.serverport=configs["server_port"]
        self.local_sock=socket.socket()
        self.local_sock.bind((self.serverip,self.serverport))
        self.local_sock.listen(define.MAXLISTENING)
        print("local bind well.")
        self.threads=[]
        self.sem=threading.Semaphore(define.MAXLISTENING)

    def __del__(self):
        pass
    def send(self,sock,data):
        s= sock.send(rc4(self.prepwd,data))
        #print("rc4 send sock")
        #print(s)
        return s
    def recv(self,sock,buffsize=define.BUFFERSIZE):
        r= rc4(self.prepwd,sock.recv(buffsize))
        #print("rc4 decrypto recv ")
        #print(r)
        return r
    def run(self):
        while True:
            client_sock,client_addr=self.local_sock.accept()
            th =threading.Thread(target=self.loop,args=[client_sock,client_addr])
            th.start()
            self.threads.append(th)

    def loop(self,client_sock,client_addr):
        try:
            login_infos=self.recv(client_sock)

            if login_infos!=bytes(self.hellopkt,encoding="utf8"):
                self.send(client_sock,bytes("error!!"))
                client_sock.close()
                return
            else:
                self.send(client_sock,bytes("good!!",encoding="utf8"))
            print("good!client has login now.")
            infos=self.recv(client_sock)
            if infos[2]==b'\x02':
                print(infos)
            port=struct.unpack("!H",infos[2:4])[0]
            ip=struct.unpack("!I",infos[4:8])[0]
            dst_host_port=port
            dst_host_ip=socket.inet_ntoa(struct.pack('I',socket.htonl(ip)))
            try:
                dst_host_sock=socket.socket()
                dst_host_sock.connect((dst_host_ip,dst_host_port))
                self.send(client_sock,bytes('nice',encoding="utf8"))
                print("connect host well.",dst_host_ip,dst_host_port)
            except:
                self.send(client_sock,b'')
                client_sock.close()
                print("connect host fail.",dst_host_ip,dst_host_port)
                return
            th =threading.Thread(target=self.recv_fromclient,args=[client_sock,dst_host_sock])
            self.sem.acquire()
            th.start()
            th2 =threading.Thread(target=self.recv_from_dsthost,args=[client_sock,dst_host_sock])
            self.sem.acquire()
            th2.start()
            self.threads.append(th)
            self.threads.append(th2)
        except:
            pass
    def recv_fromclient(self,client_sock,dst_host_sock):
        while True:
            try:
                print("prepare recv from client.")
                info =self.recv(client_sock)
                if len(info)==0:
                    client_sock.close()
                    self.self.sem.release()
                    return
                print("recv from client.")
                #print(info)
                data=info
                dst_host_sock.send(data)
                print("send to dst host.")
            except:
                self.sem.release()
                return

    def recv_from_dsthost(self,client_sock,dst_host_sock):
        while True:
            try:
                print("prepare recv from dst host.")
                dst_host_recv=dst_host_sock.recv(define.BUFFERSIZE)
                if len(dst_host_recv)==0:
                    dst_host_sock.close()
                    self.sem.release()
                    return
                print("recv from dst host.")
                print(dst_host_recv)
                self.send(client_sock,dst_host_recv)
                print("send to client.")
            except:
                self.sem.release()
                return
coolsocks_server=server(configs)
coolsocks_server.run()