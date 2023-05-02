import sys
import json
from utilities.tools import classify_image_process


def handler(event, context):
    # Get the data from the request
    # Extract the image data and model_name
    print("event:", event)
    print("type(event):", type(event))

    body_string = event.get('body')
    print("body_string:", body_string)
    body = json.loads(body_string)
    print("body:", body)
    print("type(body):", type(body))

    image_data = body.get('image_data')
    model_name = body.get('model_name')
    print("image_data:", image_data)
    print("type(image_data):", type(image_data))
    print("model_name:", model_name)
    print("type(model_name):", type(model_name))
    # Convert the base64 image data to bytes
    top3_predictions = classify_image_process(image_data, model_name)

    return top3_predictions
