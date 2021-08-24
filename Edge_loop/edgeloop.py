import json
import cv2
import time
import datetime
import logging
import random
import onnxruntime
import json
import numpy as np
from Prescription_image import *
from spreading_map import *

with open ("/home/nordluft_xaviernx/Desktop/Precision_Project/input.json",'r') as f:
    jsondata = json.load(f)
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

logger = logging.getLogger('scope.name')
logger.setLevel('DEBUG')
curr_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
file_log_handler = logging.FileHandler('logs/Edgeloop_' + curr_time + '.log')
logger.addHandler(file_log_handler)
stdout_log_handler = logging.StreamHandler()
logger.addHandler(stdout_log_handler)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_log_handler.setFormatter(formatter)
stdout_log_handler.setFormatter(formatter)



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
        return frame
    if start and time.time() - start_time >= timer: #<---- time based triggered img
        img_name = "{}{}.jpg".format(img_save_path,img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_counter))
        start_time = time.time()
        img_counter += 1
        return frame

def load_model():
    onnx_session = onnxruntime.InferenceSession("/home/nordluft_xaviernx/Downloads/trial.onnx")
    return onnx_session

def run_onnx(frame_num, onnx_session):
    img_save_path = "/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset/junfeng/sumod/train/"
    frame = cv2.imread(img_save_path +"{}.jpg".format(frame_num+50), cv2.COLOR_BGR2RGB).astype(np.float32)
    model_img_input = np.expand_dims(frame,axis = 0)
    onnx_inputs = {onnx_session.get_inputs()[0].name: model_img_input}
    onnx_output = onnx_session.run(None, onnx_inputs)[0]
    prediction_frame = onnx_output[0,:,:,0]
    return prediction_frame


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
    # print (spreader_rpm)
    return spreader_rpm





if __name__ == '__main__':
    t1 = time.time()
    run = load_model()
    t2 = time.time()
    logger.info("Time to load model initially :"+ str(t2-t1))
    img2cap = 0
    while img2cap <= 30:
        tic = time.time()
        time.sleep(1) #to simulate the delay of the camera capture 
        predicted_frame = run_onnx(img2cap,run)
        percent_masked(predicted_frame,num_pixels)
        severity_index = random.randint(0.00,100.00)
        toc2 = time.time()
        logger.info("Response_time :"+ str(toc2-tic))
        logger.info("The severity index of the image is :"+ str(severity_index))
        rpm = severity_kg_ha(severity_index)
        logger.info("Spreader RPM"+ str(rpm))
        # overlayed_img = overlay_img(number_severitylevels,frame,height,width,severity_index)
        img2cap += 1
        if img2cap == 50:
            break
