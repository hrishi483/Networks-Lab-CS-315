import threading
import socket
import rsa
import os
import json
import cv2
import sys


host = '127.0.0.1'
port = 59002
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
size = 4096

clients = []
aliases = []
alias_keys = dict()
name_key = dict()
lock = threading.Lock()  # Lock for protecting shared data

path = os.getcwd()

def broadcast(message):
    for client in clients:
        client.send(message.encode('utf-8'))

def broadcast2(message):
    if not isinstance(message, bytes):
        message = message.encode('utf-8')
    # print(type(message))
    for client in clients:
        client.send(message)



def handle_client(client):
    while True:
        try:
            message = client.recv(size)
            message=message.decode('utf-8')
            if message == "QUIT":
                index = clients.index(client)
                alias = aliases[index]
                print(f'{alias} has left the chat room')

                broadcast(f'{alias} has left the chat room')
                del alias_keys[alias]
                del name_key[alias]

                clients.remove(client)
                aliases.remove(alias)
                client.send('BYE'.encode())
                client.close()
                sys.exit(0)
                # break
            elif message == "VIDEO":
                all_files = os.listdir(path) 
                video_files = [file for file in all_files if file.endswith('.mp4')]               
                video_list = ",".join(video_files)
                client.send(b'VIDEO:'+video_list.encode('utf-8'))
                print(video_list)
            
            elif message[:4] == 'PLAY':
                all_files = os.listdir(path) 
                # Filter the list to include only files with the ".mp4" extension
                video_files = [file for file in all_files if file.endswith('.mp4')]
                prefix = message[4:].strip()
                # print(matching_files)
                matching_files = [os.path.join(path, filename) for filename in os.listdir(path) if filename.startswith(prefix)]
                print(matching_files)
                
                # print("73")

                print(f"Playing Video {matching_files[0]} in different resolutions" )
                video_path = os.path.join(path, matching_files[0])
                video_capture = cv2.VideoCapture(video_path)
                total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
                video_capture.release()

                client.send(b'TOTAL'+str(total_frames).encode('utf-8'))
                print("Total",total_frames)
                # Open the video file
                start_frame = 0
                end_frame = 0
                print("Matching",matching_files)
                resoltuion_chunk_size = (total_frames+len(matching_files)-1)//len(matching_files)
                
                for i,video in enumerate(matching_files): 
                    video_path = os.path.join(path, matching_files[i])
                    
                    video_capture = cv2.VideoCapture(matching_files[i])

                    start_frame = resoltuion_chunk_size *i
                    end_frame = min(resoltuion_chunk_size *(i+1), total_frames)
                    video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

                    current_frame = start_frame
                    # current_frame = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))
                    while current_frame < end_frame:
                        ret, frame = video_capture.read()
                        if not ret:
                            break
                        # Encode frame to JPEG
                        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                        result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
                        if not result:
                            continue
                        frame_size = len(encoded_frame)
                        f = frame_size.to_bytes(8, byteorder='big')
                        client.sendall(f)
                        client.recv(1024)
                        client.sendall(encoded_frame)
                        current_frame+=1
                    video_capture.release()
                    print("Start = ",start_frame,"End = ",end_frame,video)
                        


                    # print(f"Playing Video {matching_files[i]} ",end=" , " )
                    # residue = total_frames%len(matching_files)
                    # fpv = total_frames//len(matching_files)
                    # # print(matching_files[i])
                    # for alpha in range(0 , residue):
                    #     ret , frame = cap.read()
                    #     if not ret : 
                    #         break 
                    #     encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                    #     result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
                    #     if not result:
                    #         continue
                    #     frame_size = len(encoded_frame)
                    #     f = frame_size.to_bytes(8, byteorder='big')
                    #     client.sendall(f)
                    #     client.sendall(encoded_frame)
                    #     start_frame += 1
                    # cap.release()
                    # print("Residue sent")

                    # video_capture = cv2.VideoCapture(video_path)

                    # start_frame = fpv*i
                    # end_frame = residue + fpv*(i+1)
                    # print("start_frame: ", start_frame, " end_frame: ", end_frame, "total_frames: ", total_frames)
                    # while video_capture.isOpened():
                        
                    #     if  current_frame >= end_frame:
                    #         break
                        # Send frame size
                        
                    
                print("Video Streaming Completed")
            elif message=="HI" or message=="OK":
                    continue
            else:
                # for client in clients:
                #     client.send("HI".encode('utf-8'))
                # print("Broad",message)
                
                broadcast(message)
        # except 
        except Exception as e:
            # print(f'Error: {e}')
            # print("Type: ",type(message))
            print("*"*50)
            # print(e)
            broadcast2(message)
            # break

def receive():
    while True:
        print('server is running and listening ....')
        client,address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('Enter your name: '.encode('utf-8'))
        alias = client.recv(size).decode('utf-8')
        aliases.append(alias)

        client.send('Enter the public key: '.encode('utf-8'))
        public_key = rsa.PublicKey.load_pkcs1(client.recv(2048))
        name_key[alias] = public_key
        public_key_str = public_key.save_pkcs1().decode('utf-8')
        clients.append(client)

        alias_keys[alias] = public_key
        name_key[alias] = public_key_str
        name_key_json = json.dumps(name_key)
        # print(name_key_json)
        # message = client.recv(size).decode('utf-8')

        client.send('You are now connected!'.encode('utf-8')+ name_key_json.encode('utf-8'))
        broadcast2(f'{alias} has connected to chat room |alias:{alias} ; public key:'.encode('utf-8') + public_key.save_pkcs1("PEM"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == '__main__':
    receive()
