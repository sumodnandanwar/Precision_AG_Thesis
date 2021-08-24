import socket
import os
import time
import cv2
# import onnxruntime
import json
import numpy as np
from Prescription_image import  percent_masked
from spreading_map import  spreader_feed,image_cover

"""Global Var"""
####### Establish Connection
## device's IP address
SERVER_HOST = "192.168.45.189"
SERVER_PORT = 5001
BUFFER_SIZE = 4096   ## receive 4096 bytes each time
SEPARATOR = "<SEPARATOR>"


with open ("/home/pi/Edge_cloud/input.json",'r') as f:
    jsondata = json.load(f)

# def initialization_loop(): i.e need to run only once
width = jsondata["inputs"]["capture_size"][0]
height = jsondata["inputs"]["capture_size"][1]
num_pixels = width*height
number_severitylevels = 10
altitude = jsondata["inputs"]["Flying_altitude"]
sensor_size = jsondata["inputs"]["Sensor_size"]
focal_length = jsondata["inputs"]["focal_length"]
feed_rate = jsondata["inputs"]["Spreader_feedrate"]
feed_rpm = jsondata["inputs"]["Spreader_rpm"]

img_field_area  = image_cover(altitude,sensor_size,focal_length)[1]

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



def start_server():
    #initiate connection    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_addr = (socket.gethostname(), 2019)  #change here for sending to another machine in LAN
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    client, address = s.accept()
    print(f"Connection from {address} has been established!")
    return client


def recv_data(client):
    # receive using client socket, not server socket
    received = client.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    print(filesize)
    # convert to integer
    filesize = int(float(filesize))
    # start receiving the file from the socket
    # and writing to the file stream
    with open(filename, "wb") as f:
        while filesize:
            # read 1024 bytes from the socket (receive)
            bytes_read = client.recv(BUFFER_SIZE)
            filesize -= len(bytes_read)
            if not bytes_read:    # nothing is received
                break             # file transmitting is done
            # write to the file the bytes we just received
            f.write(bytes_read)
            file_saved = True            ##File received and saved
    return file_saved

def run_onnx():
    # model_img_input = np.expand_dims(frame,axis = 0)
    # onnx_session = onnxruntime.InferenceSession("/home/nordluft_xaviernx/Downloads/trial.onnx")
    # onnx_inputs = {onnx_session.get_inputs()[0].name: model_img_input}
    # onnx_output = onnx_session.run(None, onnx_inputs)[0]
    # prediction_frame = onnx_output[0,:,:,0]
    test_imgpt = "/home/pi/Edge_cloud/0.jpg"
    predicted_frame = cv2.imread(test_imgpt)
    return predicted_frame

####### Sending Processed Prescription value
def send_value(val,imgno):
    print("Sending the prediction value "+ str(val) + " for img number "+ str(imgno))
    client.sendall(bytes(str(val) ,"utf-8"))

client = start_server()

######## Send Messages
#Send message to client to notify about sending image
client.sendall(bytes("I'm ready, Start sending image." ,"utf-8"))
print("Server ready to receive images")

file_saved = recv_data(client)
### Sending ack of received img
if file_saved:
    client.sendall(bytes("ACK","utf-8"))

#wait for reply from client
print("Image received calculating prediction value")
# time.sleep(3) ## simulates running model

predicted_frame = run_onnx()
severity_index = percent_masked(predicted_frame,num_pixels)

def severity_kg_ha(severity_index):
    if severity_index <= 10.000:
        dose = jsondata["inputs"]["level_kg/ha"]['0']
    elif severity_index > 10.000 and severity_index <= 20.000:
        dose = jsondata["inputs"]["level_kg/ha"]['1']
    elif severity_index > 20.000 and severity_index <= 30.000:
        dose = jsondata["inputs"]["level_kg/ha"]['2']
    elif severity_index > 30.000 and severity_index <= 40.000:
        dose = jsondata["inputs"]["level_kg/ha"]['3']
    elif severity_index > 40.000 and severity_index <= 50.000:
        dose = jsondata["inputs"]["level_kg/ha"]['4']
    elif severity_index > 50.000 and severity_index <= 60.000:
        dose = jsondata["inputs"]["level_kg/ha"]['5']
    elif severity_index > 60.000 and severity_index <= 70.000:
        dose = jsondata["inputs"]["level_kg/ha"]['6']
    elif severity_index > 70.000 and severity_index <= 80.000:
        dose = jsondata["inputs"]["level_kg/ha"]['7']
    elif severity_index > 80.000 and severity_index <= 90.000:
        dose = jsondata["inputs"]["level_kg/ha"]['8']
    elif severity_index > 90.000 and severity_index <= 100.000:
        dose = jsondata["inputs"]["level_kg/ha"]['9']

    spreader_rpm = spreader_feed(dose,102,800,img_field_area)
    return spreader_rpm



rpm = severity_kg_ha(severity_index)
send_value(rpm,0)

## Acknowledgement for prediction value
ack_from_client = wait_for_acknowledge(client,"ACK")
if ack_from_client != "ACK":
    raise ValueError('Client does not acknowledge Prescription Value.')

mission_done = False
####### Closing Communication
if mission_done:
    print("All images sent.\nClosing connection.")
    client.close()
