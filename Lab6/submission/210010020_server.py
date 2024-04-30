import socket
import random

HEADER = 4
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5058
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

server_name =  socket.gethostname()  # Change this to your server's name
server_num = random.randint(1, 100)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"Connected to {addr}")
    
    data_length = conn.recv(HEADER).decode(FORMAT).strip()
    data = conn.recv(int(data_length)).decode(FORMAT)
    
    client_name, client_num = data.split()
    client_num = int(client_num)
    
    print(f"i)  Client: {client_name}, Server: {server_name}")
    print(f"ii) Client Number: {client_num}, Server Number: {server_num} Sum: {client_num + server_num}")
    print(f"")
    
    response = f"{server_name} {server_num}"
    response_length = str(len(response)).encode(FORMAT)
    response_length += b' ' * (HEADER - len(response_length))
    conn.send(response_length)
    conn.send(response.encode(FORMAT))
    
    if client_num < 1 or client_num > 100:
        print("iv) Client number out of range. Terminating connection.")
        return -1
        conn.close()
    else: 
        return 1

def start():
    server.listen()
    print(f"Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        if handle_client(conn, addr)==-1:
            break

start()
