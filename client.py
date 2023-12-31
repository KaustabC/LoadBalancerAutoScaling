from __future__ import print_function
import logging
import socket
import grpc
import trial_1_pb2
import trial_1_pb2_grpc
import random
import sys

if len(sys.argv) <2 or len(sys.argv) > 2:
        print("error, please enter port number of your tenant as the only command line argument")
        sys.exit()
logging.basicConfig(
    filename="client.log", format="%(asctime)s %(message)s", filemode="w"
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# IP_addr_intermediate = "172.17.63.199"
IP_addr_intermediate = "localhost"
port_intermediate = sys.argv[1]


def get_self_ip():
    try:
        # Create a socket object and connect to a remote host (e.g., Google's DNS server)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        # Get the local IP address
        self_ip = s.getsockname()[0]
        return self_ip
    except socket.error as e:
        print(f"Error: {e}")
        return None
    finally:
        s.close()


def run():
    ip = get_self_ip()
    print("Select from the following services: ")
    print("0. Echo")
    print("1. Simple interest calculation")
    print("2. Tax computation")
    print("3. EMI calculation")
    print("4. FD returns calculation")
    print("5. Currency conversion")
    function = int(input("Enter service number: "))
    logger.debug("Client is requesting function: " + str(function))
    if function == 0:
        data1 = int(input("Enter value to be echoed: "))
        logger.debug("Sending values: " + str(data1))
        with grpc.insecure_channel(
            IP_addr_intermediate + ":" + port_intermediate
        ) as channel:
            stub = trial_1_pb2_grpc.AlertStub(channel)
            response = stub.InvokeMethod(
                trial_1_pb2.function_message(data1=data1, function=function, ip=ip)
            )
            logger.debug("Echoed value: " + str(response.val))
            print("Echoed value: " + str(response.val))
    elif function == 1:
        data1 = int(input("Enter principal value: "))
        data2 = int(input("Enter tenure (in years): "))
        logger.debug("Sending values: " + str(data1) + ", " + str(data2))
        with grpc.insecure_channel(
            IP_addr_intermediate + ":" + port_intermediate
        ) as channel:
            stub = trial_1_pb2_grpc.AlertStub(channel)
            response = stub.InvokeMethod(
                trial_1_pb2.function_message(
                    data1=data1, data2=data2, function=function, ip=ip
                )
            )
            logger.debug("Simple interest: " + str(response.val))
            print("Calculated simple interest value: " + str(response.val))
    elif function == 2:
        data1 = int(input("Enter annual income: "))
        logger.debug("Sending values: " + str(data1))
        with grpc.insecure_channel(
            IP_addr_intermediate + ":" + port_intermediate
        ) as channel:
            stub = trial_1_pb2_grpc.AlertStub(channel)
            response = stub.InvokeMethod(
                trial_1_pb2.function_message(data1=data1, function=function, ip=ip)
            )
            logger.debug("Tax: " + str(response.val))
            print("Computed tax value: " + str(response.val))
    elif function == 3:
        data1 = int(input("Enter loan amount: "))
        data2 = int(input("Enter tenure (in years): "))
        logger.debug("Sending values: " + str(data1) + ", " + str(data2))
        with grpc.insecure_channel(
            IP_addr_intermediate + ":" + port_intermediate
        ) as channel:
            stub = trial_1_pb2_grpc.AlertStub(channel)
            response = stub.InvokeMethod(
                trial_1_pb2.function_message(
                    data1=data1, data2=data2, function=function, ip=ip
                )
            )
            logger.debug("EMI calculated: " + str(response.val))
            print("Computed EMI value:: " + str(response.val))
    elif function == 4:
        data1 = int(input("Enter FD amount: "))
        data2 = int(input("Enter tenure (in years): "))
        logger.debug("Sending values: " + str(data1) + ", " + str(data2))
        with grpc.insecure_channel(
            IP_addr_intermediate + ":" + port_intermediate
        ) as channel:
            stub = trial_1_pb2_grpc.AlertStub(channel)
            response = stub.InvokeMethod(
                trial_1_pb2.function_message(
                    data1=data1, data2=data2, function=function, ip=ip
                )
            )
            logger.debug("Estimated returns: " + str(response.val))
            print("Estimated returns on FD: " + str(response.val))
    elif function == 5:
        data1 = int(input("Enter money (in INR): "))
        print("The follwoing target currencies are available: ")
        print("1. USD")
        print("2. EUR")
        print("3. GBP")
        print("4. JPY")
        data2 = int(input("Enter your selection: "))
        logger.debug("Sending values: " + str(data1) + ", " + str(data2))
        with grpc.insecure_channel(
            IP_addr_intermediate + ":" + port_intermediate
        ) as channel:
            stub = trial_1_pb2_grpc.AlertStub(channel)
            response = stub.InvokeMethod(
                trial_1_pb2.function_message(
                    data1=data1, data2=data2, function=function, ip=ip
                )
            )
            logger.debug("Converted value: " + str(response.val))
            print("Converted value in the target currency: " + str(response.val))

    else:
        print("Invalid function number")
        logger.debug("Invalid function number given: " + str(function))


if __name__ == "__main__":
    
    run()
