import cv2 
import os
import numpy as np
from PIL import Image
 

def slice_img(input, xPieces, yPieces,nsizex,nsizey):
    filename, file_extension = os.path.splitext(input)
    im = Image.open(input)
    imgwidth, imgheight = im.size
    height = imgheight // yPieces
    width = imgwidth // xPieces
    for i in range(0, yPieces):
        for j in range(0, xPieces):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            a = im.crop(box)
            a = a.resize((nsizex,nsizey))
            try:
                a.save("Cropped_out/" + filename + "-" + str(i) + "-" + str(j) + file_extension)
            except:
                pass
            

