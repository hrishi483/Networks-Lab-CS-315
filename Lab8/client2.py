import socket
import ssl
from base64 import b64encode

userEmail = "smtplab23@gmail.com"
userPassword = "lmvgusmmhxkmzoti"
userDestinationEmail = "hrishikeshkarande2020@gmail.com" #input("Enter Email Destination: ")
userSubject = "Trial Mail"#input("Enter Subject: ")
userBody = "Hello this is trial" #input("Enter Message: ")
msg = '{}.\r\n I love computer networks!'.format(userBody)

# Choose a mail server (e.g. Google mail server) and call it mailserver
#Fill in start
mailserver = "smtp.gmail.com"
port = 587
#Fill in end
# Create socket called clientSocket and establish a TCP connection with
#Fill in start
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mailserver,port))
#Fill in end
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')
#account authentication
clientSocket.send("STARTTLS\r\n".encode())
clientSocket.recv(1024)
sslClientSocket = ssl.wrap_socket(clientSocket)
sslClientSocket.send("AUTH LOGIN\r\n".encode())
print(sslClientSocket.recv(1024))
sslClientSocket.send(b64encode(userEmail.encode()) + "\r\n".encode())
print(sslClientSocket.recv(1024))
sslClientSocket.send(b64encode(userPassword.encode()) + "\r\n".encode())
print(sslClientSocket.recv(1024))
# Send MAIL FROM command and print server response.
#Fill in start
mailFrom = f"Mail From:{userEmail}\r\n"   #include \r\n for all  the important commands
sslClientSocket.send(mailFrom.encode())
res = sslClientSocket.recv(1024)
print(f"Response 1:{res.decode()}")
#Fill in end
# Send RCPT TO command and print server response.
#Fill in start
rcptto = f"Mail From:{userDestinationEmail}\r\n"
sslClientSocket.send(rcptto.encode())
res = sslClientSocket.recv(1024)
print(f"Response 1:{res.decode()}")
#Fill in end
# Send DATA command and print server response.
#Fill in start
datacommand = f"Data\r\n"
sslClientSocket.send(datacommand.encode())
#Fill in end
# Send message data.
#Fill in start
sslClientSocket.send(msg.encode())
#Fill in end
# Message ends with a single period.
#Fill in start
endmsg = "\r\n.\r\n"
sslClientSocket.send(endmsg.encode())
recv5 = sslClientSocket.recv(1024)
print(recv5.decode())
#Fill in end
# Send QUIT command and get server response.
#Fill in start
quitCommand = "QUIT\r\n"
sslClientSocket.send(quitCommand.encode())
res = sslClientSocket.recv(1024)
print(res.decode())
#Fill in end
