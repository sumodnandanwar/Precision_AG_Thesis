# import socket
# import tqdm
# import os
# # device's IP address
# SERVER_HOST = "0.0.0.0"
# SERVER_PORT = 5001
# # receive 4096 bytes each time
# BUFFER_SIZE = 4096
# SEPARATOR = "<SEPARATOR>"
# # create the server socket
# # TCP socket
# s = socket.socket()
# # bind the socket to our local address
# s.bind((SERVER_HOST, SERVER_PORT))
# # enabling our server to accept connections
# # 5 here is the number of unaccepted connections that
# # the system will allow before refusing new connections
# s.listen(5)
# print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
# # accept connection if there is any
# client_socket, address = s.accept() 
# # if below code is executed, that means the sender is connected
# print(f"[+] {address} is connected.")

# def receivefile():
#     # receive the file infos
#     # receive using client socket, not server socket
#     received = client_socket.recv(BUFFER_SIZE).decode()
#     filename, filesize = received.split(SEPARATOR)
#     # remove absolute path if there is
#     filename = os.path.basename(filename)
#     # convert to integer
#     filesize = int(filesize)
#     # start receiving the file from the socket
#     # and writing to the file stream
#     progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
#     print(progress)
#     with open(filename, "wb") as f:
#         while True:
#             # read 1024 bytes from the socket (receive)
#             bytes_read = client_socket.recv(BUFFER_SIZE)
#             if not bytes_read:    
#                 # nothing is received
#                 # file transmitting is done
#                 break
#             # write to the file the bytes we just received
#             f.write(bytes_read)
#             # update the progress bar
#             progress.update(len(bytes_read))

# def sendfile(filename):
#     # the name of file we want to send, make sure it exists
#     # get the file size
#     filesize = os.path.getsize(filename)
#     # send the filename and filesize
#     s.send(f"{filename}{SEPARATOR}{filesize}".encode())
#     # start sending the file

#     progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
#     with open(filename, "rb") as f:
#         while True:
#             # read the bytes from the file
#             bytes_read = f.read(BUFFER_SIZE)
#             if not bytes_read:
#                 # file transmitting is done
#                 break
#             # we use sendall to assure transimission in 
#             # busy networks
#             s.sendall(bytes_read)
#             # update the progress bar
#             progress.update(len(bytes_read))

# receivefile()
# time.sleep(2)
# sendfile("/home/nordluft_xaviernx/Desktop/Precision_Project/Potato_trained_model/_DSC9666.JPG")

# # # close the client socket
# # client_socket.close()
# # # close the server socket
# # s.close()

# import socket

# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Bind the socket to the port
# server_address = ('localhost', 10000)
# print('Starting up on {} port {}'.format(*server_address))
# sock.bind(server_address)

# # Listen for incoming connections
# sock.listen(1)

# while True:
#     # Wait for a connection
#     print('waiting for a connection')
#     connection, client_address = sock.accept()
#     try:
#         print('connection from', client_address)

#         # Receive the data in small chunks and retransmit it
#         while True:
#             data = connection.recv(16)
#             print('received {!r}'.format(data))
#             if data:
#                 print('sending data back to the client')
#                 connection.sendall(data)
#             else:
#                 print('no data from', client_address)
#                 break

#     finally:
#         # Clean up the connection
#         print("Closing current connection")
#         connection.close()


# import socket
# from os import listdir
# from re import findall
# # from utility import wait_for_acknowledge

# def wait_for_acknowledge(client,response):
#     """
#     Waiting for this response to be sent from the other party
#     """
#     amount_received = 0
#     amount_expected = len(response)
    
#     msg = str()
#     while amount_received < amount_expected:
#         data = client.recv(16)
#         amount_received += len(data)
#         msg += data.decode("utf-8")
#         #print(msg)
#     return msg


# dir =  listdir("/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/Late Blight_jpg/")

# """Global Var"""
# buff_size = 4096
# fileList = [file for file in dir if findall(r'.jpg',file) != []]  #include all .jpg photos in that directory
# #fileList = ['jihyo.jpg','dami.jpg','uju.jpg']   #images to be sent over to client


# # # device's IP address
# SERVER_HOST = "192.168.148.176"
# SERVER_PORT = 5001
# # # receive 4096 bytes each time
# BUFFER_SIZE = 4096 

# #initiate connection    
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # server_addr = (socket.gethostname(), 2019)  #change here for sending to another machine in LAN
# s.bind((SERVER_HOST, SERVER_PORT))
# s.listen(5)


# # SEPARATOR = "<SEPARATOR>"
# # # create the server socket
# # # TCP socket
# # s = socket.socket()
# # # bind the socket to our local address
# # s.bind((SERVER_HOST, SERVER_PORT))

# client, address = s.accept()
# print(f"Connection from {address} has been established!")

# #Send message to client to notify about sending image
# print("Server sending command: \"Start sending image.\"")
# client.sendall(bytes("I'm ready, Start sending image." ,"utf-8"))

# #wait for reply from client
# print("Server is now waiting for acknowledge from client.")
# ack_from_client = wait_for_acknowledge(client,"ACK")
# if ack_from_client != "ACK":
#     raise ValueError('Client does not acknowledge command.')

# #Send message to client to notify about sending image
# imgCount = len(fileList)
# print("Server sends the number of images to be transfered client.")
# client.sendall(bytes(str(imgCount) ,"utf-8"))

# #wait for reply from client
# print("Server is now waiting for acknowledge from client.")
# ack_from_client = wait_for_acknowledge(client,"ACK")
# if ack_from_client != "ACK":
#     raise ValueError('Client does not acknowledge img count.')
    

# print("Server will now send the images.",end='')
# for file in fileList:
    
#     img = open(file, 'rb')
#     b_img = img.read()
#     imgsize = len(b_img)        
#     client.sendall(bytes(str(imgsize) ,"utf-8"))
#     print(f"\t sending image {file} size of {imgsize}B.")
    
#     print("Server is now waiting for acknowledge from client.")
#     ack_from_client = wait_for_acknowledge(client,"ACK")
#     if ack_from_client != "ACK":
#         raise ValueError('Client does not acknowledge img size.')
#     client.sendall(b_img)
#     img.close()
#     print(f"Image {file} sent!")
    
#     print("Server is now waiting for acknowledge from client.")
#     ack_from_client = wait_for_acknowledge(client,"ACK")
#     if ack_from_client != "ACK":
#         raise ValueError('Client does not acknowledge image transfer completion.')

 
# print("All images sent.\nClosing connection.")
# client.close()


import socket
import os
import tqdm
import time

def wait_for_acknowledge(client,response):
    """
    Waiting for this response to be sent from the other party
    """
    amount_received = 0
    amount_expected = len(response)
    
    msg = str()
    while amount_received < amount_expected:
        data = client.recv(16)
        amount_received += len(data)
        msg += data.decode("utf-8")
        #print(msg)
    return msg



"""Global Var"""
####### Establish Connection
## device's IP address
SERVER_HOST = "192.168.148.176"
SERVER_PORT = 5001
BUFFER_SIZE = 4096   ## receive 4096 bytes each time
SEPARATOR = "<SEPARATOR>"


#initiate connection    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_addr = (socket.gethostname(), 2019)  #change here for sending to another machine in LAN
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

client, address = s.accept()
print(f"Connection from {address} has been established!")


######## Send Messages
#Send message to client to notify about sending image
client.sendall(bytes("I'm ready, Start sending image." ,"utf-8"))
print("Server ready to receive images")


# receive using client socket, not server socket
received = s.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)
# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        print("r1")
        # read 1024 bytes from the socket (receive)
        bytes_read = client.recv(BUFFER_SIZE)
        if not bytes_read:    # nothing is received
            break             # file transmitting is done
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
filer = 1


## Ack for image received completely
if filer == 1:
    client.sendall(bytes("ACK" ,"utf-8"))

#wait for reply from client
print("Image received calculating prediction value")
time.sleep(3)

####### Sending Processed Prescription value
def send_value(val,imgno):
    print("Sending the prediction value for img number %s.", imgno)
    client.sendall(bytes(str(val) ,"utf-8"))

send_value(0.85,52)

## Acknowledgement for prediction value
ack_from_client = wait_for_acknowledge(client,"ACK")
if ack_from_client != "ACK":
    raise ValueError('Client does not acknowledge Prescription Value.')

####### Closing Communication
print("All images sent.\nClosing connection.")
client.close()
