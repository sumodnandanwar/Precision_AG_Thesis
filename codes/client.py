# import socket
# import time
# import tqdm
# import os

# SEPARATOR = "<SEPARATOR>"
# BUFFER_SIZE = 4096 # send 4096 bytes each time step
# # the ip address or hostname of the server, the receiver
# host = "192.168.148.176"
# # the port, let's use 5001
# port = 5001

# # create the client socket
# s = socket.socket()
# print(f"[+] Connecting to {host}:{port}")
# s.connect((host, port))
# print("[+] Connected.")

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

# sendfile("/home/nordluft_xaviernx/Desktop/Precision_Project/server.py")
# time.sleep(2)

# def receivefile():
#     # receive the file infos
#     # receive using client socket, not server socket
#     received = s.recv(BUFFER_SIZE).decode()
#     filename, filesize = received.split(SEPARATOR)
#     # remove absolute path if there is
#     filename = os.path.basename(filename)
#     # convert to integer
#     filesize = int(filesize)
#     # start receiving the file from the socket
#     # and writing to the file stream
#     progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
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

# receivefile()
## close the socket
# s.close()



import socket
import time
import tqdm
import os

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

#initiate connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

BUFFER_SIZE = 4096 # send 4096 bytes each time step
host = "192.168.148.176"
port = 5001
SEPARATOR = "<SEPARATOR>"

print(f"[+] Connecting to {host}:{port}")
client.connect((host, port))
print("[+] Connected.")

count = 1

def sendfile(filename):
    # get the file size
    filesize = os.path.getsize(filename)
    # send the filename and filesize
    client.send(f"{filename}{SEPARATOR}{filesize}".encode())
    with open(filename, "rb") as f:
        while filesize:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            filesize -= len(bytes_read)
            if not bytes_read:
                # file transmitting is done
                print('an image sent')
                break
            client.sendall(bytes_read)
    # count += 1
    # return count


#listening to server command
print("Client is checking if server is ready")
cmd_from_server = wait_for_acknowledge(client,"I'm ready, Start sending image.")

sendfile('/home/nordluft_xaviernx/Desktop/Precision_Project/cam2server.py')
print("Number of images sent %s",count)

### Checking prediction value
ack_from_client = wait_for_acknowledge(client,"ACK")
if ack_from_client == "ACK": 
    try:
        Prediction_value = float(wait_for_acknowledge(client,str(3)))
        print("Waiting for the Prediction Value %s",Prediction_value)        
    except:
        raise ValueError("Prediction Value received is buggy.")

 
if Prediction_value >= 0:
    print("Sending ACK...")
    client.sendall(bytes("ACK","utf-8"))


print("Closing connection.")
client.close()
