import socket
import random

HEADER = 4
SERVER = "127.0.0.1"  # Change this to your server's IP address
PORT = 5058
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

client_name = "Client"  # Change this to your client's name
client_num = random.randint(1, 100)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Send client name and number to server
message = f"{client_name} {client_num}"
message_length = str(len(message)).encode(FORMAT)
message_length += b' ' * (HEADER - len(message_length))
client.send(message_length)
client.send(message.encode(FORMAT))

# Receive response from server
response_length = client.recv(1024).decode(FORMAT)
response = client.recv(int(response_length)).decode(FORMAT)
print("iii) Response from server:", response)

client.close()
