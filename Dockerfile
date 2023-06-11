# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir requests


# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD monitor_push_users.py /app

# Run the script when the container launches
CMD ["python", "/app/monitor_push_users.py"]

