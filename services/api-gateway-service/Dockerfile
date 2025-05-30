# Use an official Python runtime as a parent image.
# We're using a slim-buster image for a smaller footprint.
FROM python:3.10-slim-buster

# Set the working directory in the container.
# All subsequent commands will run relative to this directory.
WORKDIR /app

# Copy the requirements.txt file into the container at /app.
# This step is done early to take advantage of Docker layer caching.
# If requirements.txt doesn't change, this layer is reused.
COPY requirements.txt .

# Install any dependencies specified in requirements.txt.
# Use --no-cache-dir to prevent pip from storing downloaded packages, reducing image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container at /app.
# This copies your 'app' folder (containing main.py) into the WORKDIR.
COPY app/ ./app/

# Expose port 8000.
# This informs Docker that the container listens on the specified network port at runtime.
EXPOSE 8000

# Define the command to run the application when the container starts.
# 'uvicorn' is the ASGI server for FastAPI.
# --host 0.0.0.0 makes the server listen on all available network interfaces.
# --port 8000 specifies the port.
# 'app.main:app' refers to the 'app' variable in 'main.py' inside the 'app' directory.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
