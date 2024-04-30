import threading
import socket
import rsa
import cv2
import sys
import numpy as np
import json
import os


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59002))
public_key, private_key = rsa.newkeys(1024)
new_keys = dict()
clients = dict()
lock = threading.Lock()  # Lock for protecting new_keys dictionary
size = 4096
alias = ""
total_frames = 0
running = False

# quit_flag = False

def is_encrypted(message, private_key):
    # print(message)
    if message[:9] == b"ENCRYPTED":
        try:
            decrypted_message = rsa.decrypt(message[9:], private_key)
            return decrypted_message.decode('utf-8'),True
        except:
            decrypted_message="This is not for you!"
            return decrypted_message,True
    else:
        if message[:6] == b"FRAMES":
            frame_size = int.from_bytes(message[6:], byteorder='big')
            print("FRAMES"+str(frame_size),type(frame_size))
            return "FRAMES"+str(frame_size),False
        try:
            return message.decode(),False
        except:
            return message,False
            print(".")


def client_receive(client):
    global alias
    global new_keys
    global total_frames
    while True:
        # try:
            encrypt = False
            
            message = client.recv(size)
            message, encrypt = is_encrypted(message, private_key)
            # print('53', message, encrypt)

            if not encrypt and message == 'Enter your name: ':
                alias = input(f'{message} ')
                client.send(alias.encode('utf-8'))

            elif not encrypt and message == 'Enter the public key: ':
                print(message, end="\n")
                try:
                    client.send(public_key.save_pkcs1("PEM"))
                    

                except Exception as e:
                    print(".")
            
            elif message == 'Quit':
                print("Bye...")
                # os._exit(0)
                sys.exit(0)

            if message == 'BYE':
                print("Bye...")
                sys.exit(0)
                
                os._exit(0)


            elif not encrypt and message[:22] == 'You are now connected!':
                # print(message)
                message,name_key_json = message.split('!')
                print(message, end="\n")
                json_data = name_key_json
                new_keys = json.loads(json_data)
                client.recv(size)

            elif not encrypt and message[:6] != "FRAMES" and 'has left the chat room' in message:
                print(message, end="\n")
                alias_left = message.split(' ')[0]
                with lock:
                    del new_keys[alias_left]
                # print(new_keys, end="\n")

            elif not encrypt and 'has connected to chat room' in message:
                m1, m2 = message.split('|')
                print(m1)
                Alias, Key = m2.split(';')
                aliass = Alias.split(':')[1].strip()
                key_t = Key.split(':')[1].strip()
                # key = rsa.PublicKey.load_pkcs1(key_t)
                key = key_t
                new_keys[aliass] = key
                print(aliass)
                print("After New Joining",new_keys.keys())

            
            
            elif not encrypt and message[:6]=="VIDEO:":
                videos = message[6:]
                video_list = videos.split(',')  # Split the string into a list of video names

                for idx, video in enumerate(video_list):
                    print(f"{idx}: {video}")  # Print each video with its index
                print("*" * 20)
            elif not encrypt and message[:4] == "PLAY":
                print(message)
                # client.send(message.encode('utf-8'))
            elif message[:5] == "TOTAL":
            # elif not encrypt and message[:5] == 'TOTAL':
                # print("96")
                total_frames = int(message[5:])
                print("TOTAL ",total_frames)
                for i in range(0,total_frames):
                    # Receive frame size
                    frame_size_bytes = client.recv(8)
                    # print('107',frame_size_bytes)
                    if not frame_size_bytes:
                        break
                    frame_size = int.from_bytes(frame_size_bytes, byteorder='big')
                    # print(frame_size,"int")
                    
                    # Receive frame data
                    frame_data = b''
                    client.send('OK'.encode()) #Extra
                    while len(frame_data) < frame_size:
                        # print(len(frame_data))
                        # chunk = client.recv(min(frame_size - len(frame_data), 8192*16))
                        chunk = client.recv(min(frame_size - len(frame_data), 4096))

                        
                        # print('chunk: ',chunk)
                        if not chunk:
                            print("Iteration",i)
                            break
                        frame_data += chunk
                    # print('Frame')
                    # print(frame_data)
                    # Decode frame
                    if len(frame_data) == frame_size:
                        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                        frame = cv2.resize(frame ,(540,260), interpolation=cv2.INTER_AREA)
                        cv2.imshow('Received Frame', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                cv2.destroyAllWindows()
                print("Video Completed Streaming...")
            else:
                print(message)
                # pass
        # except Exception as e:
        #     pass



def client_send():
    global alias
    global new_keys
    while True:
        # print("87")
        message = input("")
        if message.upper() == 'QUIT':
            client.send(message.encode('utf-8'))
            sys.exit(0)
            
            break
        elif message == 'VIDEO':
            client.send(message.encode('utf-8'))
        elif message[:4] == 'PLAY':
            client.send(message.encode('utf-8'))
            print('Request Playing ', message[4:])

        else:   
            print(f"{new_keys.keys()}")
            partner = input("Select whom to send message to ")
            try:
                if partner in new_keys.keys():
                    partner_key = new_keys[partner]
                    partner_key = rsa.PublicKey.load_pkcs1(partner_key)
                    new_message = f'{alias}: {message}'
                    encrypted_message = rsa.encrypt(new_message.encode('utf-8'), partner_key)
                    # print(encrypted_message)
                    client.send(b'ENCRYPTED'+encrypted_message)
                else:
                    print(f'{partner} not in chatroom')
            except Exception as e:
                print(".")
                # for key,aliass in new_keys.items():
                    # print(f'{key}: {aliass}')
                # print("Error sending", e)

receive_thread = threading.Thread(target=client_receive, args=(client,))
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
