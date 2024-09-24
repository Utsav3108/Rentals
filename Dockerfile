# Use the official Python image from DockerHub
FROM python:3.9

# Set the working directory inside the container
WORKDIR /rentals

# Copy the requirements file to the container
COPY ./requirements.txt /rentals/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /rentals/requirements.txt

# Copy the rest of the FastAPI application code
COPY ./main.py /rentals/main.py
COPY ./app /rentals/app


# Command to run Uvicorn App
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]
