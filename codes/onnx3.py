import keras
from keras2onnx import convert_keras
from engine import *
# onnx_path = 'uneto.onnx'
# engine_name = 'uneto.plan'
# batch_size = 1
# CHANNEL = 3
# HEIGHT = 256
# WIDTH = 256

# model = keras.models.load_model('/home/nordluft_xaviernx/Downloads/unetsmtry.h5',compile=False)

# onx = convert_keras(model, onnx_path)
# with open(onnx_path, "wb") as f:
#   f.write(onx.SerializeToString())

# shape = [batch_size , HEIGHT, WIDTH, CHANNEL]
# engine = build_engine(onnx_path, shape= shape)
# save_engine(engine, engine_name)


# import engine as eng
# import argparse
# from onnx import ModelProto
# import tensorrt as trt 

# engine_name = 'unet50.plan'
# onnx_path = "/home/nordluft_xaviernx/Downloads/unetmodelsmtry.onnx"
# batch_size = 1 

# model = ModelProto()
# with open(onnx_path, "rb") as f:
#     model.ParseFromString(f.read())

# d0 = model.graph.input[0].type.tensor_type.shape.dim[1].dim_value
# d1 = model.graph.input[0].type.tensor_type.shape.dim[2].dim_value
# d2 = model.graph.input[0].type.tensor_type.shape.dim[3].dim_value
# shape = [batch_size , d0, d1 ,d2]
# print(shape)
# engine = eng.build_engine(onnx_path, shape= shape)
# eng.save_engine(engine, engine_name) 


# import engine as eng
# import inference as inf
# import keras
# import tensorrt as trt 
# import cv2
# from PIL import Image
# import numpy as np

# input_file_path = '/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/Late Blight_jpg/Late_Blight (449).jpg'
# onnx_file = "/home/nordluft_xaviernx/Downloads/unetmodelsmtry.onnx"
# serialized_plan_fp32 = "semantic.plan"
# HEIGHT = 256
# WIDTH = 256

# image = np.asarray(Image.open(input_file_path))
# im = np.array(image, dtype=np.float32, order='C')

# engine = eng.load_engine(trt_runtime, serialized_plan_fp32)
# h_input, d_input, h_output, d_output, stream = inf.allocate_buffers(engine, 1, trt.float32)
# out = inf.do_inference(engine, im, h_input, d_input, h_output, d_output, stream, 1, HEIGHT, WIDTH)

# cv2.imshow("Out",out)
# cv2.waitKey(0)
# colorImage_trt = Image.fromarray(out.astype(np.uint8))
# colorImage_trt.save(“trt_output.png”)


# import numpy as np
# from keras.preprocessing import image
# from keras.applications.resnet50 import preprocess_input
# # import keras2onnx
# import onnxruntime

# # image preprocessing
# img_path = '/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/Late Blight_jpg/Late_Blight (449).jpg'   # make sure the image is in img_path
# img_size = 256
# img = image.load_img(img_path, target_size=(img_size, img_size))
# x = image.img_to_array(img)
# x = np.expand_dims(x, axis=0)
# x = preprocess_input(x)

# # load keras model
# from keras.applications.resnet50 import ResNet50
# model = ResNet50(include_top=True, weights='imagenet')

# # convert to onnx model
# onnx_model = "/home/nordluft_xaviernx/Downloads/unetmodelsmtry.onnx"

# # runtime prediction
# content = onnx_model.SerializeToString()
# sess = onnxruntime.InferenceSession(content)
# x = x if isinstance(x, list) else [x]
# feed = dict([(input.name, x[n]) for n, input in enumerate(sess.get_inputs())])
# pred_onnx = sess.run(None, feed)

# import onnx
# import argparse
# import onnx_tensorrt.backend as backend
# import numpy as np
# import time

# def main():
#     parser = argparse.ArgumentParser(description="Onnx runtime engine.")
#     parser.add_argument(
#         "--onnx", default="/home/arkenstone/test_face_model/res50/mxnet_exported_mnet.onnx",
#         metavar="FILE",
#         help="path to onnx file",
#     )
#     parser.add_argument(
#         "--shape",
#         default="(1,3,112,112)",
#         help="input shape for inference",
#     )
#     args = parser.parse_args()
# model = onnx.load(args.onnx)
# engine = backend.prepare(model, device='CUDA:0')
# shape_str = args.shape.strip('(').strip(')')
# input_shape = []
# for item in shape_str.split(','):
#     input_shape.append(int(item)) 
# input_data = np.random.random(size=input_shape).astype(np.float32)
# start = time.time()
# cal = []
# for i in range(110):
#     output_data = engine.run(input_data)[0]
#     cal.append(time.time())
# end = time.time()
# total_time = end - start
# print("Total Runtimetime {:.4f} seconds".format(total_time))
# start = cal[10]
# Per_time = ( end -start ) / 100.0
# print("Per iter runtime: {:.4f} seconds".format(Per_time))
    
# if __name__ == "__main__":
#     print ("Usage: .... ")
#     print ("python tensorrt_run.py --onnx your.onnx --shape (1,3,112,112)")
#     main()

