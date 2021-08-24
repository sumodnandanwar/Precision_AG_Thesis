
from PIL import Image, ImageOps 
import numpy as np 
import cv2   

Number_of_Health_level = 10

red_mask = (0, 0, 255)
coralred_mask = (80, 127, 255)
orange_mask = (0, 165, 255)
goldenrod_mask = (32, 165, 218)
Yellow_mask = (0, 255,255)
Yellowgreen_mask = (50, 205, 154)
lime_mask = (0, 255, 0)
green_mask = (0, 128, 0)
lightseagreen_mask = (170,178,32)
navy_mask = (128, 0, 0)

colour_list = [red_mask,coralred_mask,orange_mask,
               goldenrod_mask,Yellow_mask,
               Yellowgreen_mask,lime_mask,
               green_mask,lightseagreen_mask,navy_mask]



def get_image_size(img_path):
    image = Image.open(img_path)
    #Size returns a 2-tuple, containing the horizontal and vertical size in pixels.
    height, width = image.size
    num_pixels = height * width
    return num_pixels,height,width

def blackpng_to_rgb(img_path,save_path = None):
    img = Image.open(img_path)
    img = img.convert('RGB')
    img = ImageOps.autocontrast(img)
    # To save image the converted image
    if save_path is not None: 
        img.save(save_path)
    else:
        pass 
    return img


def percent_masked(img_path,num_pixels): 
    # img = cv2.imread(img_path)
    im = cv2.sumElems(img_path)
    total_mask =  im[2]
    percent_mask = (total_mask/num_pixels) * 1000 # Gives 18% insead of 8
    percent_mask = round(percent_mask, 3)
    if percent_mask < 0:
        percent_mask = 0.0
    elif percent_mask >= 100:
        percent_mask = 100
    return percent_mask


def overlay_img(Number_of_Health_level,image,height,width,percent_mask):
    # image = cv2.imread(img_path)
    overlay = image.copy()
    output = image.copy()
    if Number_of_Health_level == 5:
        if percent_mask <= 20.000:
            colour_overlay = colour_list[9]
        elif percent_mask > 20.000 and percent_mask <= 40.000:
            colour_overlay = colour_list[7]
        elif percent_mask > 40.000 and percent_mask <= 60.000:
            colour_overlay = colour_list[5]
        elif percent_mask > 60.000 and percent_mask <= 80.000:
            colour_overlay = colour_list[3]
        elif percent_mask > 80.000 and percent_mask <= 100.000:
            colour_overlay = colour_list[0]

    if Number_of_Health_level == 10:
        if percent_mask <= 10.000:
            colour_overlay = colour_list[9]
        elif percent_mask > 10.000 and percent_mask <= 20.000:
            colour_overlay = colour_list[8]
        elif percent_mask > 20.000 and percent_mask <= 30.000:
            colour_overlay = colour_list[7]
        elif percent_mask > 30.000 and percent_mask <= 40.000:
            colour_overlay = colour_list[6]
        elif percent_mask > 40.000 and percent_mask <= 50.000:
            colour_overlay = colour_list[5]
        elif percent_mask > 50.000 and percent_mask <= 60.000:
            colour_overlay = colour_list[4]
        elif percent_mask > 60.000 and percent_mask <= 70.000:
            colour_overlay = colour_list[3]
        elif percent_mask > 70.000 and percent_mask <= 80.000:
            colour_overlay = colour_list[2]
        elif percent_mask > 80.000 and percent_mask <= 90.000:
            colour_overlay = colour_list[1]
        elif percent_mask > 90.000 and percent_mask <= 100.000:
            colour_overlay = colour_list[0]
            

    #select the region that has to be overlaid
    rect = cv2.rectangle(overlay, (0, 0), (height, width),colour_overlay, -1)
    alpha = 0.45 #Adding the transparency parameter
    #Performing image overlay
    output = cv2.addWeighted(overlay, alpha, output, 1 - alpha,0, output)
    #To Save the overlaid image
    # cv2.imwrite('Output'+str(alpha) +'.jpg', output)

    # cv2.imshow("Out",output)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return output

# num_pixels,height,width = get_image_size('/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/trial_img/label/35.png')
# num = percent_masked('/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/trial_img/label/35.png',num_pixels)
# img = blackpng_to_rgb('/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/trial_img/label/35.png')
# overlay_img(10,img,height,width,num)
# print(num)

