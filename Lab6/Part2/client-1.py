import socket 
import time
import numpy as np
import random

HEADER = 64
PORT = 9999
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "QUIT"
SERVER = "10.200.92.157"
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
	msg = msg.encode(FORMAT)
	msg_length = len(msg)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' '*(HEADER-len(send_length))  #+= forget
	client.send(send_length)
	client.send(msg)
	

	msg = client.recv(HEADER).decode(FORMAT)
	if msg:
		print(msg)
		server_num,server_name = msg.split()
		return server_num


rand_num = str(random.randint(1,100))
client_name = socket.gethostname()
client_str = rand_num+" "+client_name

while True:
	server_num = send(client_str)
	client_name = socket.gethostname()
	client_str = server_num+" "+client_name


