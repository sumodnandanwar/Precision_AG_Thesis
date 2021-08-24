import socket
import time
import os
import logging
# import onnxruntime
import json
import numpy as np
from Prescription_image import *
from spreading_map import *

BUFFER_SIZE = 4096 # send 4096 bytes each time step
host = "192.168.45.189"
port = 5001
SEPARATOR = "<SEPARATOR>"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

output_file_handler = logging.FileHandler("output.log")
stdout_handler = logging.StreamHandler()

logger.addHandler(output_file_handler)
logger.addHandler(stdout_handler)

formatter = logging.Formatter('%(asctime)s - %(message)s')
output_file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)

def start_client():
    #initiate connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # keep track of connection status  
    connected = False  
    # print( "connected to server" )  
    print(f"[+] Connecting to {host}:{port}")
    logger.debug(f"[+] Connecting to {host}:{port}")
    while not connected:
        try:
            client.connect((host, port))
            logger.debug("[+] Connected.")
            print("[+] Connected.")
            connected = True
        except socket.error:
            pass
    return client

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

def sendfile(filename,client):
    # get the file size
    filesize = os.path.getsize(filename)
    # print (filename,filesize)
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

def capture_save(trig,start):
    capture = cv2.VideoCapture(0)
    capture.set(3, 640) ## Set capture resolution
    capture.set(4, 480)
    start_time = time.time()
    img_counter = 0
    timer = 2   ### Sets timer to every 2 seconds
    img_save_path = "/home/sumod/Work/Prescription map Thesis/Codes/Edge_loop/captured_img/"
    ret, frame = capture.read()  ##returns frame of shape (w,h,3)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32)
    ## To show the frames
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) ##Gray needed else gets black
    # cv2.imshow('frame', gray)
    ## TO exit command using key q
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    if trig:
        img_name = "{}{}.jpg".format(img_save_path,img_counter)
        cv2.imwrite(img_name, frame)
        img_counter += 1
    if start and time.time() - start_time >= timer: #<---- time based triggered img
        img_name = "{}{}.jpg".format(img_save_path,img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_counter))
        start_time = time.time()
        img_counter += 1
    return img_counter


client = start_client()

#listening to server command
print("Client is checking if server is ready")
cmd_from_server = wait_for_acknowledge(client,"I'm ready, Start sending image.")

img_counter = capture_save(True,False)

##send saved img
sendfile("/home/sumod/Work/Prescription map Thesis/Codes/Edge_loop/captured_img/{}.jpg".format(img_counter-1),client)
print("Number of images sent ",img_counter)

### Checking prediction value
ack_from_client = wait_for_acknowledge(client,"ACK")
if ack_from_client == "ACK": 
    try:
        Prediction_value = float(wait_for_acknowledge(client,str(3)))
        logger.debug("Waiting for the Prediction Value ",Prediction_value)
        print("Waiting for the Prediction Value ",Prediction_value)        
    except:
        logger.debug("Prediction Value received is buggy.")
        raise ValueError("Prediction Value received is buggy.")
 
if Prediction_value >= 0:
    # print("Sending ACK...")
    client.sendall(bytes("ACK","utf-8"))


mission_done = False
if mission_done:
    print("Closing connection.")
    client.close()

