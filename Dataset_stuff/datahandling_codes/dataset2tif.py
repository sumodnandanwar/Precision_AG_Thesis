import os
import time
import sys
import cv2
# from convert2tif.convert2tif import convert

# Converts all the files in the path foldet to .tif
pathin = '/home/nordluft_xaviernx/Desktop/Precision_Project/Potato_trained_model/_DSC9666.JPG'
pathout = "/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/label/"
# convert(pathin,pathout)
# time.sleep(2)

# Rename files in folder
# folder = pathout
# files = os.listdir(folder)
#Alphanumeric sorting
# import re
# def sorted_alphanumeric(data):
#     convert = lambda text: int(text) if text.isdigit() else text.lower()
#     alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
#     return sorted(data, key=alphanum_key)
# #Sorts the file in numeric order instead of lexigraphic
# files = sorted(files, key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
# # print (files)
# counter = 1101
# for fi, file in enumerate(files):
#     # os.rename(folder + file, folder + str(fi)+".tif")
#     os.rename(folder + file, folder + str(counter)+".png")
#     counter += 1

img = cv2.imread('/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/trial_img/label/809.png')
cv2.imshow("Out",img)
cv2.waitKey(0)