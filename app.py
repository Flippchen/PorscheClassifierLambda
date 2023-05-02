import sys
import json
from utilities.tools import classify_image_process


def handler(event, context):
    # Get the data from the request
    # Extract the image data and model_name
    print('event: ', event)
    body_string = event.get('body')
    body = json.loads(body_string)

    image_data = body.get('image_data')
    model_name = body.get('model_name')
    # Convert the base64 image data to bytes
    top3_predictions = classify_image_process(image_data, model_name)

    return top3_predictions
