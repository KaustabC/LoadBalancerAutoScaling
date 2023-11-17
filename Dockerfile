# Use the official Python image from the Docker Hub
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the server code and protobuf files to the container
COPY . /app

# Install required dependencies
RUN pip install grpcio
RUN pip install grpcio-tools

# Expose the port on which the gRPC server runs
EXPOSE 50051

# Set the environment variable for Python to run the server code
CMD ["python", "end.py"]