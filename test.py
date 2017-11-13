import socket
sock=socket.socket()
sock.bind(("127.0.0.1",9090))
sock.listen(100)
while True:
	client,clientadd=sock.accept()
	info=client.recv(1024)
	print(info)
	client.send(b'\x00\x5a'+info[2:8])
	info=client.recv(1024)
	print(info)	
	client.close()

