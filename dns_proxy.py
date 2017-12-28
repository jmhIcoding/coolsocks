__author__ = 'jmh081701'
import socket
import threading
dns_server="8.8.8.8"
dns_port=53
class dnsproxy:
    def __init__(self,dns_server,dns_port=53,local_addr="127.0.0.1",local_port=53):
        self.dns_server=dns_server
        self.dns_port=dns_port
        self.remote_dns_addr=(dns_server,dns_port)
        self.proxy_sock=socket.socket(type=socket.SOCK_DGRAM)
        self.proxy_sock.bind((local_addr,local_port))
        self.buffersize=1024
        self.threads=[]
        self.maxthreads=1024
        self.thread_sem=threading.Semaphore(self.maxthreads)

    def loop(self,iedata,ieaddr):
        self.thread_sem.acquire()
        #print(ieaddr)
        #print("dns request:"+str(iedata))
        remote_sock=socket.socket(type=socket.SOCK_DGRAM)
        remote_sock.sendto(iedata,self.remote_dns_addr)
        remote_data,remote_add=remote_sock.recvfrom(self.buffersize)
        #print(remote_add)
        #print(str(remote_data))
        local_sock=socket.socket(type=socket.SOCK_DGRAM)
        local_sock.sendto(remote_data,ieaddr)
        self.thread_sem.release()
    def server_run(self):
        while True:
            iedata,ieaddr=self.proxy_sock.recvfrom(self.buffersize)
            th = threading.Thread(target=self.loop,args=[iedata,ieaddr])
            th.start()
            self.threads.append(th)
    def local_run(self):
        pass
'''
dns=dnsproxy(dns_server)
dns.run()
'''