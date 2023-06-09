# PorscheClassifierLambda

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Flippchen/PorscheClassifierLambda?include_prereleases&style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Flippchen/PorscheClassifierLambda/build_and_deploy.yaml?style=flat-square)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Flippchen/PorscheClassifierlambda?style=flat-square)


## Overview
This repository contains the AWS Lambda function for the [PorscheInsight-CarClassification-AI project](https://github.com/Flippchen/PorscheInsight-CarClassification-AI), which classifies Porsche cars based on their images. The Lambda function is built using AWS Lambda and the Python 3.10 runtime. It handles the image classification process by utilizing the pre-trained AI models from the main [PorscheInsight-CarClassification-AI](https://github.com/Flippchen/PorscheInsight-CarClassification-AI) repository.

The Lambda function is designed to be simple and easy to deploy, allowing users to access the car classification service from anywhere in the world.


## Features
- AWS Lambda function for image classification
- Compatible with Python 3.10 runtime
- Utilizes pre-trained AI models for Porsche car classification
- Easy deployment and integration with AWS services

## Prerequisites
- An AWS account with access to AWS Lambda, API Gateway, and other necessary services
- Docker for building the Lambda function container image
- Python 3.9 or higher for local testing (optional)

## Deployment
1. Clone this repository to your local machine.
2. Navigate to the repository directory.
3. Build the Docker image:
```
docker build . -t porscheinsight-lambda
```
4. Create an Amazon Elastic Container Registry (ECR) repository, if you haven't already:
```
aws ecr create-repository --repository-name porscheinsight-lambda
```
5. Authenticate Docker to your Amazon ECR registry:
```
aws ecr get-login-password --region <your_aws_region> | docker login --username AWS --password-stdin <your_account_id>.dkr.ecr.<your_aws_region>.amazonaws.com
```
6. Tag the Docker image:
```
docker tag porscheinsight-lambda:latest <your_account_id>.dkr.ecr.<your_aws_region>.amazonaws.com/porscheinsight-lambda:latest
```
7. Push the Docker image to Amazon ECR:
```
docker push <your_account_id>.dkr.ecr.<your_aws_region>.amazonaws.com/porscheinsight-lambda:latest
```
8. Create a new AWS Lambda function and set its "Function package" to use the container image you just pushed to Amazon ECR.
9. Set function variables in AWS Lambda Connsole:
```
NUMBA_CACHE_DIR=/tmp
```
## Usage
You can integrate the Lambda function with AWS API Gateway to expose a public REST API, which allows users to send images for classification.

The Lambda function expects a JSON object with the following format:
```
{
  "image": "<base64_encoded_image>",
    "model_type": "<model_name>"
}
```
## Disclaimer
This is not an official Porsche product and is not affiliated with or endorsed by Porsche AG.





