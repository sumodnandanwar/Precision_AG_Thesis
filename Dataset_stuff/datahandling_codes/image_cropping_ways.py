import cv2 
import os
import numpy as np
from PIL import Image
 
# image = cv2.imread("_DSC9666.JPG")
# cv2.imshow("Big",image)
# y=0
# x=0
# h=512
# w=512
# crop_image = image[x:w, y:h]
# cv2.imshow("Cropped", crop_image)
# cv2.waitKey(0)


infile = '/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/junfeng/train1/20.jpg'
# chopsize = 30

# img = Image.open(infile)
# width, height = img.size

# # Save Chops of original image
# for x0 in range(0, width, chopsize):
#    for y0 in range(0, height, chopsize):
#       box = (x0, y0,
#              x0+chopsize if x0+chopsize <  width else  width - 1,
#              y0+chopsize if y0+chopsize < height else height - 1)
#       print('%s %s' % (infile, box))
#       img.crop(box).save('zchop.%s.x%03d.y%03d.jpg' % (infile.replace('.jpg',''), x0, y0))

def imgcrop(input, xPieces, yPieces):
    filename, file_extension = os.path.splitext(input)
    im = Image.open(input)
    imgwidth, imgheight = im.size
    height = imgheight // yPieces
    width = imgwidth // xPieces
    for i in range(0, yPieces):
        for j in range(0, xPieces):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            a = im.crop(box)
            try:
                a.save("/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/Cropped_out/" + "-" + str(i) + "-" + str(j) + file_extension)
                print('Saving Crops!!!')
            except:
                pass

imgcrop(infile, 2, 2)