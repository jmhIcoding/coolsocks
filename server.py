#coding:utf8
__author__ = 'jmh081701'
from crypto.rc4 import  rc4
import socket
import  define
import  config
import  threading
import  struct
configs=config.get_config()
prepwd=configs["password"]
hellopkt=configs["hello"]
serverip=configs["server_ip"]
serverport=configs["server_port"]
localip=configs["local_ip"]
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
        return sock.send(rc4(self.prepwd,data))
    def recv(self,sock,buffsize=define.BUFFERSIZE):
        return rc4(self.prepwd,sock.recv(buffsize))
    def run(self):
        client_sock,client_addr=self.local_sock.accept()
        th =threading.Thread(target=self.loop,args=[client_sock,client_addr])
        th.start()
        self.threads.append(th)

    def loop(self,client_sock,client_addr):
        try:
            login_infos=self.recv(client_sock)
            if login_infos!=self.hellopkt:
                self.send(client_sock,bytes("error!!"))
                client_sock.close()
                return
            else:
                self.send(client_sock,bytes("good!!"))
            infos=self.recv(client_sock)
            print(infos)
            port=struct.unpack("!H",infos[2:4])[0]
            ip=struct.unpack("!I",infos[4:8])[0]
            dst_host_port=port
            dst_host_ip=socket.inet_ntoa(struct.pack('I',socket.htonl(ip)))
            print(dst_host_ip,dst_host_port)
            try:
                dst_host_sock=socket.socket()
                dst_host_sock.connect((dst_host_ip,dst_host_port))
                self.send(client_sock,bytes('nice'))
            except:
                self.send(client_sock,b'')
                client_sock.close()
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
                dst_host_recv=dst_host_sock.recv(define.BUFFERSIZE)
                if len(dst_host_recv)==0:
                    dst_host_sock.close()
                    self.sem.release()
                    return
                print("recv from dst host.")
                self.send(client_sock,dst_host_recv)
                print("send to client.")
            except:
                self.sem.release()
                return
coolsocks_server=server()
coolsocks_server.run()