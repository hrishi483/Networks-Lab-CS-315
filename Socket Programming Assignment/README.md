# Socket Programming Assignment  

## Demo Video Link: https://www.youtube.com/watch?v=FikX3PoClww

## File Structure:
1. Unzip the file submitted with name 210010020.zip
2. Place the videos (with .mp4 extension) that you want to run in the same folder as the python files, with the resolution as extension. Eg.wildlife_144p.mp4, wildlife_360p.mp4 and wildlife_720p.mp4. 
3. To start execution of the code first run the 210010020_server.py this starts the server. 
4. Now execute the 210010020_client.py to start the clients.

## Instructions to run 
1. A Windows machine is preffered for executing this assignments. 
2. Unzip the file and navigate to the folder containing the files using `cd path\to\project\directory`.
3. Install the requirements using the command `pip install -r requirements.txt`. 
4. To run the server `python .\210010020_server.py`.
5. Now run the clients using `python .\210010020_client.py`.
6. Instructions :
- To send a message to any available client Type the message and then select whom to send the message to .
- To get a list of available videos, enter the command `VIDEO` Without any available spaces.
- To play a video you need to enter the video name without specifying it's resolution `PLAY Video_name`. Eg PLAY wildlife
to stream the video.


## Explanation of the code 
#### Server Code Explanation

#### Functions

##### `broadcast(message)`
- Broadcasts a message to all connected clients.
- Parameters:
  - `message`: The message to be broadcasted.
- Sends the message to each client in the `clients` list.

##### `broadcast2(message)`
- Variant of `broadcast` function.
- Sends a message to all clients, ensuring it's encoded in UTF-8 format.
- Parameters:
  - `message`: The message to be broadcasted.

##### `handle_client(client)`
- Handles communication with a specific client.
- Listens for messages from the client and takes appropriate actions based on the message received.
- Manages client disconnection and removal from the chat room.
- Parameters:
  - `client`: The socket object representing the client connection.

##### `receive()`
- Main function to accept incoming connections from clients.
- Accepts connections, prompts clients to enter their name and public key, and adds them to the chat room.
- Spawns a new thread to handle each client's communication.
- Starts listening for incoming connections.

#### Client Code Explanation



#### Key Components

- **Socket Initialization**: 
  - The script initializes a socket object for client-server communication using the TCP/IP protocol.

- **Key Generation**:
  - The client generates a public-private key pair using the RSA algorithm to ensure secure communication with the server.

- **Connection Establishment**:
  - The client establishes a connection with the server using the server's IP address and port number.

#### Functions

#### Message Encryption and Decryption

- Messages sent between the client and server are encrypted using the recipient's public key to ensure confidentiality.
- Upon receiving messages from the server, the client decrypts them if necessary to process them appropriately.

#### Message Reception

- A separate thread (`client_receive`) continuously listens for incoming messages from the server.
- Messages are decrypted if necessary and processed accordingly:
  - User input prompts for alias and public key entry.
  - Handling of connection status messages, such as client joining or leaving the chat room.
  - Displaying available videos and playing requested videos.
  - Receiving and displaying video frames.

#### Message Sending

- Another thread (`client_send`) handles user input for sending messages to other clients.
- Messages are encrypted using the recipient's public key before being sent to the server.
- User input includes options to quit, request video listing, and send messages to specific clients.


---