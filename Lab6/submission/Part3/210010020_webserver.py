import socket
import os

def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode("utf-8")
    if request_data:
        request_lines = request_data.split("\r\n")
        request_method = request_lines[0].split(" ")[0]
        file_path = request_lines[0].split(" ")[1]

        if request_method == "GET":
            if file_path == "/":
                file_path = "/index.html"  
            file_path = file_path[1:]  

            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    file_content = file.read()
                    response_headers = "HTTP/1.1 200 OK\r\n\r\n"
                    client_socket.send(response_headers.encode("utf-8") + file_content)
            else:
                response_headers = "HTTP/1.1 404 Not Found\r\n\r\n"
                client_socket.send(response_headers.encode("utf-8"))
        else:
            # Only support GET method for now
            response_headers = "HTTP/1.1 501 Not Implemented\r\n\r\n"
            client_socket.send(response_headers.encode("utf-8"))

    client_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening on port", port)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection from:", client_address)
        handle_request(client_socket)

    server_socket.close()

if __name__ == "__main__":
    HOST = "127.0.0.1"  # Your server's IP address
    PORT = 6789
    start_server(HOST, PORT)
