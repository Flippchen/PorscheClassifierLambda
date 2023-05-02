import sys
import json
from utilities.tools import classify_image_process


def handler(event, context):
    # Get the data from the request
    # Extract the image data and model_name
    body = json.loads(event.get('body'))

    image_data = body.get('image_data')
    model_name = body.get('model_name')
    print(body)
    # Convert the base64 image data to bytes
    top3_predictions = classify_image_process(image_data, model_name)

    return top3_predictions
