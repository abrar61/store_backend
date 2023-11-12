# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install software-properties-common default-libmysqlclient-dev -y

# Create and set the working directory
WORKDIR /store_backend

# Copy the requirements file into the container at /store_backend
COPY requirements.txt /store_backend/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --no-deps

# Copy the current directory contents into the container at /store_backend
COPY . /store_backend/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
