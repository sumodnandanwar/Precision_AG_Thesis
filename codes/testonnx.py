import numpy as np

import onnx
from onnx import numpy_helper
from onnx import mapping
from onnx import TensorProto
import onnxruntime as rt


def create_random_data(shape, type, minvalue, maxvalue, seed):
    nptype = np.dtype(type)
    np.random.seed(seed)
    return ((maxvalue - minvalue) * np.random.sample(shape) + minvalue).astype(nptype)


if __name__ == '__main__':
    model_path = "/home/nordluft_xaviernx/Downloads/trial.onnx"
    m = onnx.load(model_path)
    input_dict = {}
    output_names = []
    for i in m.graph.input:
        shape_arr = []
        shape_obj = i.type.tensor_type.shape
        for onedim in shape_obj.dim:
            if onedim.HasField("dim_param"):
                shape_arr.append(1)
            if onedim.HasField("dim_value"):
                shape_arr.append(onedim.dim_value)
        print("input name: ", i.name, " shape: ", shape_arr)
        # TODO convert type from proto to numpy type
        d = create_random_data(shape_arr, np.float32, 0, 1, None)
        input_dict[i.name] = d

    for o in m.graph.output:
        output_names.append(o.name)

    print("number of inputs: ", len(input_dict))
    print("outputs: ", output_names)

    # rt.set_default_logger_severity(0)
    sess = rt.InferenceSession(model_path)

    res = sess.run(output_names, input_dict)
    print("result: ", res)