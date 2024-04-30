import socket
import time
server_address = ('localhost', 12000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1)  # 1 second timeout

for i in range(10):
    message = f'Ping {i + 1}'
    start_time = time.time()
    client_socket.sendto(message.encode(), server_address)
    try:
        response, server = client_socket.recvfrom(1024)
        end_time = time.time()  
        rtt = end_time - start_time  # Calculate RTT
        print(f'Response from server: {response.decode()}, RTT: {rtt:.6f} seconds')
    except socket.timeout:
        print('Request timed out')


client_socket.close()
