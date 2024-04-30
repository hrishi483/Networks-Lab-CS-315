import socket
import ssl
from base64 import b64encode

userEmail = "smtplab23@gmail.com"
userPassword = "lmvgusmmhxkmzoti"
# userDestinationEmail = "hrishikeshkarande2020@gmail.com"
userDestinationEmail = input("Enter Email Destination: ")
userSubject = input("Enter Subject: ")
userBody = input("Enter Message: ")
msg = f'To:{userDestinationEmail}\r\nFrom:{userEmail}:\r\nSubject:{userSubject}\r\n\r\n{userBody} \r\n I love computer networks!\r\n .\r\n'.format(userDestinationEmail,userEmail,userSubject,userBody)

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com'
mailport = 587

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mailserver, mailport))

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

# Account authentication
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
mailFromCommand = f"MAIL FROM: <{userEmail}>\r\n"
sslClientSocket.send(mailFromCommand.encode())
recv2 = sslClientSocket.recv(1024)
print(recv2.decode())

# Send RCPT TO command and print server response.
rcptToCommand = f"RCPT TO: <{userDestinationEmail}>\r\n"
sslClientSocket.send(rcptToCommand.encode())
recv3 = sslClientSocket.recv(1024)
print(recv3.decode())

# Send DATA command and print server response.
dataCommand = "DATA\r\n"
sslClientSocket.send(dataCommand.encode())
recv4 = sslClientSocket.recv(1024)
print(recv4.decode())

# Send message data.
sslClientSocket.send(msg.encode())

# Message ends with a single period.
endmsg = "\r\n.\r\n"
sslClientSocket.send(endmsg.encode())
recv5 = sslClientSocket.recv(1024)
print(recv5.decode())

# Send QUIT command and get server response.
quitCommand = "QUIT\r\n"
sslClientSocket.send(quitCommand.encode())
recv6 = sslClientSocket.recv(1024)
if recv6.decode()!='221':
    print(recv6.decode())
else:
    print('221 Not received from server')

sslClientSocket.close()
