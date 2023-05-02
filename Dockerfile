# Use the official Python image as the base image
FROM public.ecr.aws/lambda/python:3.10

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

ENV U2NET_HOME=/tmp
# Copy the rest of the application code
COPY utilities ${LAMBDA_TASK_ROOT}/utilities
COPY app.py ${LAMBDA_TASK_ROOT}
COPY models ${LAMBDA_TASK_ROOT}/models
COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY rembg /tmp

CMD [ "app.handler" ]
