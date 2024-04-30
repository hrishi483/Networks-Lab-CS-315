# import all the libraries
'''
NOTE: Managing several connections similar to OS. Python provides 'select' to manage sockets on all OS may be Windows, Linux or Mac-OS
'''
import socket
import select

# set the global variables like: Header_length, port number and host name
HEADER_LENGTH = 10
PORT = 12345
IP = "127.0.0.1"

# creating the server socket using TCp connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Overcome the Address already in use error do the following
# Syntax: .setsockopt(solve socket connection, reuse address on PORT, True (1))
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the IP and port number
server_socket.bind((IP, PORT))

# listen to the total number of clients
server_socket.listen(5)

# manage a list of clients
sockets_list = [server_socket]

# dictionary of the clients with key as the clients socket and value is client's data
clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        # check if client closed the connection
        if not len(message_header):
            return False

        msg = message_header.decode()
        if msg == 'Quit':
            client_socket.close()
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


while True:
    # select.select(read sockets, write sockets, exception sockets)
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(f"Accepted connection from {client_address[0]}: {client_address[1]} username: {user['data'].decode('utf-8')}")

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del [notified_socket]