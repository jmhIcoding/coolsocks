#coding:utf8
__author__ = 'jmh081701'
from crypto.rc4 import  rc4
import socket
import  define
import  config
import  threading
import  struct
configs=config.get_config()

class client:
    def __init__(self,configs):
        if (configs["type"]!="client"):
            print("Please check the configure file,make sure it 's for client.")
            exit(-1)
        self.prepwd=configs["password"]
        self.hellopkt=configs["hello"]
        self.serverip=configs["server_ip"]
        self.serverport=configs["server_port"]
        self.localport=configs['local_port']
        self.threads=[]
        try:
            self.server_sock=socket.socket()
            self.server_sock.connect((self.serverip,self.serverport))

            self.server_sock.send(rc4(self.prepwd,self.hellopkt))
            #try to login in remote server
            info=self.recv(self.server_sock,define.BUFFERSIZE)
        except:
            print("Connnect server error. Please check the configure file.")
            self.server_state=False
            exit(1)
        print(info)
        if info!=bytes("good!!",encoding="utf8"):
            print("Connnect server error. Please check the configure file.")
            self.server_state=False
            exit(1)
        else:
            print("Connect server well. Enjoy yourself.")
            self.server_sock.close()
            self.server_state=True
        self.local_sock=socket.socket()
        print((define.LOCALADDRESS,self.localport))
        self.local_sock.bind((define.LOCALADDRESS,self.localport))
        self.local_sock.listen(define.MAXLISTENING)
        print("local bind well. Here goes the vacation.")

        self.sem=threading.Semaphore(define.MAXLISTENING)

    def __del__(self):
        for th in self.threads:
            th.join()

    def run(self):
        while True:
            iesock,ieaddr=self.local_sock.accept()
            th =threading.Thread(target=self.loop,args=[iesock,ieaddr])
            th.start()
            self.threads.append(th)
    def gen_server_sock(self):
        if self.server_state==False:
            exit(-1)
        server_sock=socket.socket()
        server_sock.connect((self.serverip,self.serverport))
        server_sock.send(rc4(self.prepwd,self.hellopkt))
        #try to login in remote server
        info=self.recv(server_sock,define.BUFFERSIZE)
        #print(info)
        if info!=bytes("good!!",encoding="utf8"):
            print("connnect server error. Please check the configure file.")
            exit(1)
        return server_sock
    def send(self,sock,data):
        return sock.send(rc4(self.prepwd,data))
    def recv(self,sock,buffsize=define.BUFFERSIZE):
        return rc4(self.prepwd,sock.recv(buffsize))

    def loop(self,iesock,ieaddr):
        try:
            infos=iesock.recv(define.BUFFERSIZE)
            print('from ie ',infos)
            data=infos
            server_sock=self.gen_server_sock()
            self.send(server_sock,data)
            info_from_server=self.recv(server_sock)
            if info_from_server==bytes('nice'):
                iesock.send(b'\x00\x5a'+infos[2:8])
                print("remote server can proxy this host.")
            else:
                iesock.send(b'\x00\x00'+infos[2:8])
                print("remote server can't proxy this host.")
                return

            th =threading.Thread(target=self.recv_fromie,args=[iesock,server_sock])
            self.sem.acquire()
            th.start()
            th2 =threading.Thread(target=self.recv_fromhost,args=[iesock,server_sock])
            self.sem.acquire()
            th2.start()
            self.threads.append(th)
            self.threads.append(th2)
        except:
            pass

    def recv_fromie(self,iesock,server_sock):
        while True:
            try:
                info =iesock.recv(define.BUFFERSIZE)
                if len(info)==0:
                    iesock.close()
                    self.sem.release()
                    return
                print("recv from ie")
                #print(info)
                data=info
                self.send(server_sock,data)
                print("send to host.")
            except:
                self.sem.release()
                return

    def recv_fromhost(self,iesock,server_sock):
        while True:
            try:
                server_recv=self.recv(server_sock)
                if len(server_recv)==0:
                    server_sock.close()
                    self.sem.release()
                    return
                print("recv from host.")
                iesock.send(server_recv)
                print("send to ie.")
            except:
                self.sem.release()
                return
coolsock_client=client(configs)
coolsock_client.run()