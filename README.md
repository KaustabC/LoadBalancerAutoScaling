# LoadBalancerAutoScaling
LoadBalancerAutoScaling (LBAS) is a Python-based project that leverages gRPC, protocol buffers, and Docker to seamlessly integrate intermediate servers, end servers, and clients, fostering scalability, responsiveness, and security.

This repository contains the codebase for a distributed system architecture designed for a Financial Services Deployment System that is a part of the assignment from the Semester-I '23-24 offering of the CS G527 Cloud Computing course.

## Underlying System Architecture

  ![unnamed](https://github.com/KaustabC/LoadBalancerAutoScaling/assets/74728041/88ce1e05-15b9-4068-82f0-2724525c755b)

## Requirements

- Python 3.x
- gRPC (Google Remote Procedure Call): gRPC tools and gRPC Python Libraries
- Protobuf  ‘protoc’  compiler (for .proto files)
- Docker (code was run and tested on v4.24)
- docker Python Library

Please ensure that you have these dependencies installed and configured before running the scripts.

## Running Instructions
_Note:_
_1) The operating systems of the machines on which the files are to be run must be Linux-based._
_2) Ensure that all the required software and libraries are installed on your system. For more information on which libraries and software are needed, kindly go through technical design documentation._

1) Clone the repository.
2) Create a docker image named ‘endserversleep’ via instruction:
```
docker build -t endserversleep .
```
3) Run scaler.py
```
python scaler.py
```
4) Run portal.py to register a tenant via email and password. Then choose the services, load balancer and auto scaler types.
```
python portal.py
```
5) Two containers are started as soon as a tenant deploys his services for clients to use. A port number is also issued to the tenant, which is to be passed to the client.
Run client by passing the port number (as given by tenant) as a command line argument as follows:
```
python client.py <PORT_NUMBER>
```
