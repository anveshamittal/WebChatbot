# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY req.txt req.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r req.txt

# Copy your application's source code into the container
COPY ./src ./src
COPY ./config ./config
# Note: We are NOT copying the local faiss_index anymore

# Expose the port the app runs on (e.g., 8000 for FastAPI/Uvicorn)
EXPOSE 8000

# Command to run your application
# This assumes you are using FastAPI. Adjust if you use Flask or something else.
# Your main.py should be in src/app/
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]