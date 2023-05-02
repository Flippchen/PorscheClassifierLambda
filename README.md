# Porsche Classifier Server

This is a Django web application that uses machine learning to classify images.

## Features

- Image upload and classification using a trained model
- Responsive web interface for easy interaction

## Getting Started

These instructions will help you set up the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10
- Docker (optional)

### Installation

1. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
2. Apply migrations:
    ```bash
    python manage.py migrate
    ```
3. Run the development server:
    ```bash
    python manage.py runserver 0.0.0.0:8000 --insecure
    ```
Open your browser and navigate to `http://127.0.0.1:8000/` to view the app.

### Using Docker

If you prefer to use Docker, follow these steps:

1. Build the Docker image:
    ```bash
    docker build . -t porsche:1
    ```
2. Run the Docker container:
    ```bash
    docker run -p 8000:8000 porsche:1
    ```