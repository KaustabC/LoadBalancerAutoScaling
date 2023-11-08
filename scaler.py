import logging
from concurrent import futures
import grpc
import trial_1_pb2
import trial_1_pb2_grpc
import trial_2_pb2
import trial_2_pb2_grpc
import docker

class Server(trial_1_pb2_grpc.AlertServicer):
    def __init__(self):
        self.port_end = "50051"
        self.IP_addr_end = "endserverContainer"
    def start_end_server_container(self):
        # Docker client setup
        docker_client = docker.from_env()

        # Check if End Server container is running, if not, start the container
        containers = docker_client.containers.list(all=True, filters={"name": "endserverContainer"})
        # print(containers)
        if not containers:
            docker_client.containers.run("endserver", name="endserverContainer", detach=True, network="cloudtemp")
            print("End Server container started.")
            logger.debug("End Server container started.")
        else:
            print("End Server container is already running.")
            logger.debug("End Server container is already running.")

        self.IP_addr_end = "endserverContainer"  # Update the IP address to the container name

    def InvokeMethod(self, request, context):
        #to start end server container if its not already running
        self.start_end_server_container()

        # make grpc call based on function to localhost:port_end (later can be changed to actual IP address):
        logger.debug("Received function call for function: " + str(request.function))
        if request.function == 0:
            with grpc.insecure_channel(self.IP_addr_end + ":" + self.port_end) as channel:
                stub = trial_2_pb2_grpc.AlertStub(channel)
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1, function=request.function))
                logger.debug("Echoed value: " + str(response.val))
        
        elif request.function == 1:
            with grpc.insecure_channel(self.IP_addr_end + ":" + self.port_end) as channel:
                stub = trial_2_pb2_grpc.AlertStub(channel)
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1, data2 = request.data2,function=request.function))
                logger.debug("Calculated simple interest value: " + str(response.val))

        elif request.function == 2:
            with grpc.insecure_channel(self.IP_addr_end + ":" + self.port_end) as channel:
                stub = trial_2_pb2_grpc.AlertStub(channel)
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1,function=request.function))
                logger.debug("Computed tax value: " + str(response.val))
                
        elif request.function == 3:
            with grpc.insecure_channel(self.IP_addr_end + ":" + self.port_end) as channel:
                stub = trial_2_pb2_grpc.AlertStub(channel)
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1,data2=request.data2,function=request.function))
                logger.debug("Computed emi value: " + str(response.val))
                
        elif request.function == 4:
            with grpc.insecure_channel(self.IP_addr_end + ":" + self.port_end) as channel:
                stub = trial_2_pb2_grpc.AlertStub(channel)
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1,data2=request.data2,function=request.function))
                logger.debug("Estimated returns on FD: " + str(response.val))
                
        elif request.function == 5:
            with grpc.insecure_channel(self.IP_addr_end + ":" + self.port_end) as channel:
                stub = trial_2_pb2_grpc.AlertStub(channel)
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1,data2=request.data2,function=request.function))
                logger.debug("Converted value in the target currency: " + str(response.val))
                
        return trial_1_pb2.returnValue(val = response.val)


def serve():
    # Initialising the connector server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    trial_1_pb2_grpc.add_AlertServicer_to_server(
        Server(), server
    )
    port = 50050 

    # Starting the server
    server.add_insecure_port("[::]:" + str(port))
    server.start()
    print("Server started listening on port " + str(port) + "...")
    logger.debug("Server started listening on port " + str(port) + "...")
    server.wait_for_termination()


if __name__ == "__main__":
    # Intitialising the logger
    logging.basicConfig(
        filename="scaler.log",
        format="%(asctime)s %(message)s",
        filemode="w",
    )

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.debug("check ")

    serve()