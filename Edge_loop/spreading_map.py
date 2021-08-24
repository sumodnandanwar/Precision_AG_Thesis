from PIL import Image, ImageOps 
import numpy as np
import math 
import cv2   
import json

def cal_FOV(spreader_spread):
    alp_breadth = 2*(math.atan((spreader_spread[0]/2)/spreader_spread[2]))
    alp_width = 2*(math.atan((spreader_spread[1]/2)/spreader_spread[2]))
    alp_breadth = round(math.degrees(alp_breadth),1)
    alp_width = round(math.degrees(alp_width),1)
    FOV_spread = [alp_breadth,alp_width]
    return FOV_spread


## Input the spreader spread [breadth, width, height] in metres
spreader_spread = [20,20,10]
# print("Spreader FOV in angle:"+ str(cal_FOV(spreader_spread)))


## Works only when camera mounted nadir
def image_cover(altitude,sensor_size,f_length):
    field_width = (sensor_size[0]*altitude)/f_length
    field_height = (sensor_size[1]*altitude)/f_length
    img_cover = [field_width,field_height]
    img_area = field_height*field_width
    return img_cover,img_area

altitude = spreader_spread[2]
sensor_size = [13.2,8.8]
focal_length = 8
# print ("Image field cover:" + str(image_cover(altitude,sensor_size,focal_length)[0]))
img_area  = image_cover(altitude,sensor_size,focal_length)[1]

# Raise warning if image distance less than or greater than spreader distance
def hect_2_sqm(amount):
    kg_sqm = amount/10000
    return kg_sqm


def spreader_feed(kg_ha,feedrate,feed_rpm,img_area):
    kgsqm_per_imgsqm = img_area * (kg_ha/10000) ###Gives in kg
    feed = feedrate/feed_rpm         ### feedrate in kg/min
    rev = round(kgsqm_per_imgsqm/feed) ##Gives in rpm
    return rev

# img_area  = image_cover(altitude,sensor_size,focal_length)[1]
# print(spreader_feed(1500,102,800,img_area))

    


