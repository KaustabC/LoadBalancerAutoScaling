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
EXPOSE 90090
EXPOSE 90091
EXPOSE 90092
EXPOSE 90093
EXPOSE 90094
EXPOSE 90095
EXPOSE 90096
EXPOSE 90097
EXPOSE 90098
EXPOSE 90099

# Set the environment variable for Python to run the server code
CMD ["python", "end.py"]
