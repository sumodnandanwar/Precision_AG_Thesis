import cv2
import onnxruntime
from matplotlib import pyplot as plt
import numpy as np
import time


test_imgpt = "/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/junfeng/train1/44.jpg"
# "/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/junfeng/train1/44.jpg"
gtlabelpt = "/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/junfeng/labels1/44.png"


#Input should be as float32 for onnxruntime model to work
test_img = cv2.imread(test_imgpt,cv2.COLOR_BGR2RGB).astype(np.float32) 

gtlabel = cv2.imread(gtlabelpt,0)
test_img_input = np.expand_dims(test_img,axis = 0)
gtlabel = np.expand_dims(gtlabel,-1)



onnx_session = onnxruntime.InferenceSession("/home/nordluft_xaviernx/Downloads/trial.onnx")
tic = time.clock()
onnx_inputs = {onnx_session.get_inputs()[0].name: test_img_input}
onnx_output = onnx_session.run(None, onnx_inputs)[0]
toc = time.clock()
prediction2 = onnx_output[0,:,:,0]

print(toc-tic)
# y_pred=model.predict(test_img)
# y_pred_thresholded = y_pred > 0.8

# intersection = np.logical_and(y_test, y_pred_thresholded)
# union = np.logical_or(y_test, y_pred_thresholded)
# iou_score = np.sum(intersection) / np.sum(union)
# print("IoU socre is: ", iou_score)

# test_img_input=np.expand_dims(test_img, 0)
# ground_truth=y_test[test_img_number]
# print(test_img_input.shape)


# plt.figure(figsize=(16, 8))
# plt.subplot(231)
# plt.title('Testing Image')
# plt.imshow(test_img)
# plt.subplot(232)
# plt.title('Testing Label')
# plt.imshow(gtlabel[:,:,0], cmap='gray')
# plt.subplot(233)
# plt.title('Prediction on test image')
# plt.imshow(prediction2, cmap='gray')

# plt.show()