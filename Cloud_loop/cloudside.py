import socket
import os
import time
import cv2
# import onnxruntime
import json
import numpy as np
from Prescription_image import  percent_masked
from spreading_map import  spreader_feed,image_cover


class Process_recv:
    def __init__(self):
        """Global Var"""
        ####### Establish Connection
        ## device's IP address
        self.SERVER_HOST = "192.168.120.49"
        self.SERVER_PORT = 5002
        self.BUFFER_SIZE = 4096   ## receive 4096 bytes each time
        self.SEPARATOR = "<S>"
        self.save_rcd_img = '/home/sumod/Work/Prescription map Thesis/Codes/Cloud_loop/rec_images/'

        with open ("/home/sumod/Work/Prescription map Thesis/Codes/input.json",'r') as f:
            self.jsondata = json.load(f)

        width = self.jsondata["inputs"]["capture_size"][0]
        height = self.jsondata["inputs"]["capture_size"][1]
        self.num_pixels = width*height
        number_severitylevels = 10
        altitude = self.jsondata["inputs"]["Flying_altitude"]
        sensor_size = self.jsondata["inputs"]["Sensor_size"]
        focal_length = self.jsondata["inputs"]["focal_length"]
        feed_rate = self.jsondata["inputs"]["Spreader_feedrate"]
        feed_rpm = self.jsondata["inputs"]["Spreader_rpm"]

        self.img_field_area  = image_cover(altitude,sensor_size,focal_length)[1]

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
        return msg



    def start_server(self):
        #initiate connection    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.SERVER_HOST, self.SERVER_PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(5)
        client, address = s.accept()
        print(f"Connection from {address} has been established!")
        return client


    def recv_data(self,client):
        # receive using client socket, not server socket
        # amount_received = 0
        # amount_expected = 100
        
        # msg = str()
        # while amount_received < amount_expected:
        #     data = client.recv(32).decode("utf-8")
        #     amount_received += len(data)
        #     msg += data
        #     #print(msg)
        #     received = msg
        # 'utf-8','surrogateescape'
        received = client.recv(self.BUFFER_SIZE).decode()
        filename, filesize = received.split(self.SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        filenameu = self.save_rcd_img + filename
        ##convert to integer
        filesize = int(float(filesize))
        # start receiving the file from the socket
        # and writing to the file stream
        with open(filenameu, "wb") as f:
            while filesize:
                # read 1024 bytes from the socket (receive)
                bytes_read = client.recv(filesize,self.BUFFER_SIZE)
                filesize -= len(bytes_read)
                if len(bytes_read) <= 0:    # nothing is received
                    break             # file transmitting is done
                # write to the file the bytes we just received
                f.write(bytes_read)
                file_saved = True            ##File received and saved
        return file_saved, filename

    def run_onnx(self,filename):
        # model_img_input = np.expand_dims(frame,axis = 0)
        # onnx_session = onnxruntime.InferenceSession("/home/nordluft_xaviernx/Downloads/trial.onnx")
        # onnx_inputs = {onnx_session.get_inputs()[0].name: model_img_input}
        # onnx_output = onnx_session.run(None, onnx_inputs)[0]
        # prediction_frame = onnx_output[0,:,:,0]
        test_imgpt = "/home/sumod/Work/Prescription map Thesis/Codes/Cloud_loop/rec_images/{}".format(filename)
        predicted_frame = cv2.imread(test_imgpt)
        time.sleep(0.5)
        return predicted_frame

    ####### Sending Processed Prescription value
    def send_value(self,val,imgno,client):
        print("Sending the prediction value "+ str(val) + " for"+ imgno)
        client.sendall(bytes(str(val) ,"utf-8"))


    def severity_kg_ha(self,severity_index):
        if severity_index <= 10.000:
            dose = self.jsondata["inputs"]["level_kg/ha"]['0']
        elif severity_index > 10.000 and severity_index <= 20.000:
            dose = self.jsondata["inputs"]["level_kg/ha"]['1']
        elif severity_index > 20.000 and severity_index <= 30.000:
            dose = self.jsondata["inputs"]["level_kg/ha"]['2']
        elif severity_index > 30.000 and severity_index <= 40.000:
            dose = self.jsondata["inputs"]["level_kg/ha"]['3']
        elif severity_index > 40.000 and severity_index <= 50.000:
            dose = self.jsondata["inputs"]["level_kg/ha"]['4']
        elif severity_index > 50.000 and severity_index <= 60.000:
            dose = self.jsondata["inputs"]["level_kg/ha"]['5']
        elif severity_index > 60.000 and severity_index <= 70.000:
            dose = self.jsondata["inputs"]["level_kg/ha"]['6']
        elif severity_index > 70.000 and severity_index <= 80.000:
            dose = self.jsondata["inputs"]["level_kg/ha"]['7']
        elif severity_index > 80.000 and severity_index <= 90.000:
            dose = self.jsondata["inputs"]["level_kg/ha"]['8']
        elif severity_index > 90.000 and severity_index <= 100.000:
            dose = self.jsondata["inputs"]["level_kg/ha"]['9']

        spreader_rpm = spreader_feed(dose,102,800,self.img_field_area)
        return spreader_rpm

    def main(self,client):
        ######## Send Messages
        #Send message to client to notify about sending image
        client.sendall(bytes("I'm ready, Start sending image." ,"utf-8"))
        # print("Server ready to receive images")

        file_saved,filename = self.recv_data(client)
        ### Sending ack of received img
        if file_saved:
            client.sendall(bytes("ACK","utf-8"))

        predicted_frame = self.run_onnx(filename)
        severity_index = percent_masked(predicted_frame,self.num_pixels)

        rpm = self.severity_kg_ha(severity_index)
        self.send_value(rpm,filename,client)

        ## Acknowledgement for prediction value
        ack_from_client = self.wait_for_acknowledge(client,"ACK")
        if ack_from_client != "ACK":
            raise ValueError('Client does not acknowledge Prescription Value.')

    def close_conn(self,client):
        print("Closing connection.")
        client.close()

if __name__ == '__main__':
    classs = Process_recv()
    client = classs.start_server()
    # classs.main(client)
    img2cap = 0
    while img2cap <= 30:
        classs.main(client)
        img2cap += 1
        if img2cap == 30:
            break
