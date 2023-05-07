import numpy as np
import onnxruntime as ort
from typing import List, Tuple
import base64
from io import BytesIO
from PIL import Image
from utilities.class_names import get_classes_for_model
from utilities.prepare_images import replace_background, resize_and_pad_image, fix_image

from rembg import new_session

# Initiate models
models = {
    "car_type": None,
    "all_specific_model_variants": None,
    "specific_model_variants": None,
    "pre_filter": None,
}

session = new_session("u2net")


def load_model(model_name: str) -> ort.InferenceSession:
    if model_name == "car_type":
        path = "/var/task/models/car_type.onnx"
    elif model_name == "/var/task/all_specific_model_variants":
        path = "/var/task/models/all_specific_model_variants.onnx"
    elif model_name == "/var/task/specific_model_variants":
        path = "/var/task/models/specific_model_variants.onnx"
    elif model_name == "pre_filter":
        path = "/var/task/models/pre_filter.onnx"
    else:
        raise ValueError("Invalid model name")

    return ort.InferenceSession(path, providers=['CPUExecutionProvider'])


def prepare_image(image_data: Image, target_size: Tuple, remove_background: bool) -> np.ndarray:
    if remove_background:
        image = replace_background(image_data, session=session)
    else:
        image = resize_and_pad_image(image_data, target_size)
    img_array = np.array(image).astype('float32')
    img_array = np.expand_dims(img_array, 0)
    return img_array


def get_top_3_predictions(prediction: np.ndarray, model_name: str) -> List[Tuple[str, float]]:
    top_3 = prediction[0].argsort()[-3:][::-1]
    classes = get_classes_for_model(model_name)
    top_3 = [(classes[i], round(prediction[0][i] * 100, 2)) for i in top_3]
    return top_3


def get_pre_filter_prediction(image_data: np.ndarray, model_name: str):
    if models[model_name] is None:
        models[model_name] = load_model(model_name)
    input_name = models[model_name].get_inputs()[0].name
    prediction = models[model_name].run(None, {input_name: image_data})
    filter_names = get_top_3_predictions(prediction[0], "pre_filter")
    return filter_names


def classify_image_process(image_data: str, model_name: str) -> List[Tuple[str, float]]:
    # Load model if not loaded yet
    if models[model_name] is None:
        models[model_name] = load_model(model_name)

    # Decode image and open it
    image_data = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_data))

    # Fix image orientation and color mode if needed
    image = fix_image(image)

    # Get correct input size for model
    input_size = models[model_name].get_inputs()[0].shape[1:3]

    # Prepare image for filtering and predict
    filter_image = prepare_image(image, input_size, remove_background=True)
    filter_predictions = get_pre_filter_prediction(filter_image, "pre_filter")
    # If the pre_filter predicts porsche or other_car_brand, predict the correct model
    if filter_predictions[0][0] == "porsche":
        # prepared_image = prepare_image(image, input_size, remove_background=True)
        input_name = models[model_name].get_inputs()[0].name
        prediction = models[model_name].run(None, {input_name: filter_image})
        # Get top 3 predictions
        top_3 = get_top_3_predictions(prediction[0], model_name)

        return top_3

    return filter_predictions
