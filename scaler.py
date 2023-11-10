import logging
from concurrent import futures
import grpc
import trial_1_pb2
import trial_1_pb2_grpc
import trial_2_pb2
import trial_2_pb2_grpc
import docker
from random import randint
from time import sleep

class Server(trial_1_pb2_grpc.AlertServicer):
    def __init__(self):        
        self.IP_addr_end = "localhost"
        self.containers_and_load = {}
        self.first_run = True
        self.load_balancing_type = 4
        self.round_robin_index = 0
        self.start_end_server_container()
    
    def first_free_container_port(self):
        for i in range(50051, 50060):
            if str(i) not in self.containers_and_load:
                return str(i)
    
    def add_end_server_container(self):
        docker_client = docker.from_env()
        free = self.first_free_container_port(self)
        docker_client.containers.run("endserver", name="endserverContainer"+free, detach=True, network="cloudtemp", ports={'50051/tcp':free})
        self.containers_and_load[free] = 0
        sleep(1)
        return free
    
    def start_end_server_container(self):
        logger.debug("check65")
        # Docker client setup
        docker_client = docker.from_env()
        logger.debug("check6")

        # Check if End Server container is running, if not, start the container
        containers = docker_client.containers.list(all=True, filters={"name": "endserverContainer"})
        # print(containers)
        logger.debug("check7")
        if not containers:
            free = self.first_free_container_port()
            docker_client.containers.run("endserversleep", name="endserverContainer"+free, detach=True, network="cloudtemp",ports={'50051/tcp':free})
            self.containers_and_load[free] = 0
            free = self.first_free_container_port()
            docker_client.containers.run("endserversleep", name="endserverContainer"+free, detach=True, network="cloudtemp",ports={'50051/tcp':free})
            self.containers_and_load[free] = 0
            print("Primary end server containers started.")
            logger.debug("Primary end server containers started.")
        else:
            print("Primary end server containers are already running. System must be restarted.")
            logger.debug("Primary end server containers are already running. System must be restarted.")
        logger.debug("check8")
        # self.IP_addr_end = "endserverContainer"  # Update the IP address to the container name
    
    def issueJob(self, request, port, context):
        # make grpc call based on function to localhost:port_end (later can be changed to actual IP address):
        logger.debug("Received function call for function: " + str(request.function))
        with grpc.insecure_channel(self.IP_addr_end + ":" + port) as channel:
            stub = trial_2_pb2_grpc.AlertStub(channel)
            if request.function == 0:
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1, function=request.function))
                logger.debug("Echoed value: " + str(response.val))
            
            elif request.function == 1:
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1, data2 = request.data2,function=request.function))
                logger.debug("Calculated simple interest value: " + str(response.val))

            elif request.function == 2:        
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1,function=request.function))
                logger.debug("Computed tax value: " + str(response.val))
                    
            elif request.function == 3:
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1,data2=request.data2,function=request.function))
                logger.debug("Computed emi value: " + str(response.val))
                    
            elif request.function == 4:
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1,data2=request.data2,function=request.function))
                logger.debug("Estimated returns on FD: " + str(response.val))
                    
            elif request.function == 5:
                response = stub.RelayClientMessage(trial_2_pb2.function_message(data1=request.data1,data2=request.data2,function=request.function))
                logger.debug("Converted value in the target currency: " + str(response.val))
        logger.debug("check10")

        return trial_1_pb2.returnValue(val = response.val)
    
    def InvokeMethod(self, request, context):
        # Perform load balancing here across the end server containers that are running to determine which end server to issue the job to
        
        if self.load_balancing_type == 0:
            # Least connections load balancing
            selected_port = min(self.containers_and_load, key=self.containers_and_load.get)
        
        elif self.load_balancing_type == 1:
            # Random choice
            n = randint(0, len(self.containers_and_load)-1)
            selected_port = list(self.containers_and_load.keys())[n]
            
        elif self.load_balancing_type == 2:
            # Power of two choices
            n1 = randint(0, len(self.containers_and_load)-1)
            n2 = randint(0, len(self.containers_and_load)-1)
            while n2 == n1:
                n2 = randint(0, len(self.containers_and_load)-1)
            n1 = list(self.containers_and_load.keys())[n1]
            n2 = list(self.containers_and_load.keys())[n2]
            if self.containers_and_load[n1] <= self.containers_and_load[n2]:
                selected_port = n1
            else:
                selected_port = n2
                
        elif self.load_balancing_type == 3:
            # Round robin
            selected_port = list(self.containers_and_load.keys())[self.round_robin_index % len(self.containers_and_load)]
            self.round_robin_index += 1
        
        elif self.load_balancing_type == 4:
            # IP hash
            # selected_port = list(self.containers_and_load.keys())[hash(source IP address goes here) % len(self.containers_and_load)]
            selected_port = list(self.containers_and_load.keys())[0]        # temporary
            
        print("Issuing job to end server container: " + selected_port)
        self.containers_and_load[selected_port] += 1
        return_val = self.issueJob(request, selected_port, context)
        self.containers_and_load[selected_port] -= 1
        
        return return_val


def serve():
    # Initialising the connector server
    logger.debug("check2")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logger.debug("check3")
    trial_1_pb2_grpc.add_AlertServicer_to_server(
        Server(), server
    )
    logger.debug("check4")
    port = 50050 

    # Starting the server
    server.add_insecure_port("[::]:" + str(port))
    server.start()
    logger.debug("check5")
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
    logger.debug("check1")

    serve()