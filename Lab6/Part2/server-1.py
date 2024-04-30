import socket 
import numpy as np
import threading 
import time
import random

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 9999
DISCONNECT_MESSAGE = "QUIT"
ADDR = (SERVER,PORT)
print(f"[SERVER] {SERVER}")
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn,addr):
	print(f"New Connection {addr} Connected\n")
	connected = True
	while connected:
		msg_length = conn.recv(HEADER).decode(FORMAT).strip()
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			print(f"{addr} : {msg}")
			client_num,client_name = msg.split()
			
			server_num = random.randint(1,100)
			if int(client_num) >100 :
				connected = False
				break
			else:
				server_name = socket.gethostname()
				print(f"i)Client: {client_name} Server: {server_name}")
				print(f"ii)Client {int(client_num)}, server_num: {int(server_num)} Sum: {int(client_num)+int(server_num)}")
				msg = str(server_num)+" "+server_name
				msg = msg.encode(FORMAT)
				conn.send(msg)
	conn.close()
	return_value = False
	print("Closing Server")
	

def start():
	global return_value
	server.listen()
	print(f"[Listening] Server is listening on {ADDR}")
	while True:
		conn,addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn,addr))
		thread.start()
		print(f"Active Connections = {threading.active_count()-1}\n")

		if not return_value:
			break

start()




