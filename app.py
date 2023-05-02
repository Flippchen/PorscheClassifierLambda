import sys
import json
from utilities.tools import classify_image_process


def handler(event, context):
    # Get the data from the request
    # Extract the image data and model_name
    image_data = event.get('image_data')
    model_name = event.get('model_name')
    print(event)
    # Convert the base64 image data to bytes
    top3_predictions = classify_image_process(image_data, model_name)

    return top3_predictions
