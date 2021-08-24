import socket
import time
import datetime
import os
import logging
# import onnxruntime
import json
import numpy as np
from Prescription_image import *
from spreading_map import *

# with open ("/home/pi/Edge_cloud/input.json",'r') as f:
#     jsondata = json.load(f)

class Capture_send:

    def __init__(self):
        self.BUFFER_SIZE = 4096 # send 4096 bytes each time step
        self.host = "192.168.120.49"
        self.port = 5002
        self.SEPARATOR = "<S>"
        self.img_save_path = "/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset/junfeng/sumod/train/"
        self.img_counter = 0
        self.logger = logging.getLogger('scope.name')
        self.logger.setLevel('DEBUG')
        self.curtime = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
        file_log_handler = logging.FileHandler('logs/edgeside_' + self.curtime + '.log')
        self.logger.addHandler(file_log_handler)
        stdout_log_handler = logging.StreamHandler()
        self.logger.addHandler(stdout_log_handler)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_log_handler.setFormatter(formatter)
        stdout_log_handler.setFormatter(formatter)



    def start_client(self):
        #initiate connection
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # keep track of connection status  
        connected = False  
        # print( "connected to server" )  
        print(f"[+] Connecting to {self.host}:{self.port}")
        while not connected:
            try:
                client.connect((self.host, self.port))
                print("[+] Connected.")
                connected = True
            except socket.error:
                pass
        return client

    def wait_for_acknowledge(self,client,response):
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

    def sendfile(self,filbase,filend,client):
        # get the file size
        filename = filbase+filend
        filesize = os.path.getsize(filename)
        sendname = str(filend)+self.SEPARATOR+str(filesize)
        client.send(sendname.encode('utf-8'))
        with open(filename, "rb") as f:
            while filesize:
                # read the bytes from the file
                bytes_read = f.read(self.BUFFER_SIZE)
                filesize -= len(bytes_read)
                if not bytes_read:
                    # file transmitting is done
                    print('an image sent')
                    break
                client.sendall(bytes_read)

    def capture_save(self,trig,start):
        capture = cv2.VideoCapture(0)
        capture.set(3, 640) ## Set capture resolution
        capture.set(4, 480)
        start_time = time.time()
        timer = 2   ### Sets timer to every 2 seconds
        ret, frame = capture.read()  ##returns frame of shape (w,h,3)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32)
        ## To show the frames
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) ##Gray needed else gets black
        # cv2.imshow('frame', gray)
        ## TO exit command using key q
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        if trig:
            img_name = "{}{}.jpg".format(self.img_save_path,self.img_counter)
            cv2.imwrite(img_name, frame)
            self.img_counter += 1
        if start and time.time() - start_time >= timer: #<---- time based triggered img
            img_name = "{}{}.jpg".format(self.img_save_path,self.img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(self.img_counter))
            start_time = time.time()
            self.img_counter += 1
        return self.img_counter
    def sent_saved(self):
        time.sleep(0.1) ##delay to simulate capture
        self.img_counter += 1
        return self.img_counter

    def main(self,client):
        #listening to server command
        # print("Client is checking if server is ready")
        self.wait_for_acknowledge(client,"I'm ready, Start sending image.")
        start = time.time()
        # img_counter = self.capture_save(True,False)
        img_counter = self.sent_saved()
        ##send saved img
        self.sendfile(self.img_save_path ,"{}.jpg".format(img_counter),client)
        # print("Number of images sent ",img_counter)
        self.logger.info("Number of images sent"+ str(img_counter))
        ### Checking prediction value
        ack_from_client = self.wait_for_acknowledge(client,"ACK")
        if ack_from_client == "ACK": 
            try:
                Prediction_value = float(self.wait_for_acknowledge(client,str(3)))
                # print("The Prediction Value ",Prediction_value)
                self.logger.info("The Prediction Value received"+ str(Prediction_value))        
            except:
                raise ValueError("Prediction Value received is buggy.")
        stop = time.time()
        E_Edelay = round((stop - start),3)
        # print("Cycle response time is :",E_Edelay)
        self.logger.info("Cycle response time is :" + str(E_Edelay))
        if Prediction_value >= 0:
            # print("Sending ACK...")
            client.sendall(bytes("ACK","utf-8"))

    def close_conn(self,client):
        print("Closing connection.")
        client.close()

if __name__ == '__main__':
    classs = Capture_send()
    client = classs.start_client()

    img2cap = 0
    while img2cap <= 30:
        classs.main(client)
        img2cap += 1
        if img2cap == 30:
            classs.close_conn(client)
            break



