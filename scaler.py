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
import threading
import csv


class Server(trial_1_pb2_grpc.AlertServicer):
    def __init__(self, loadType, autoScaleType, services, base, intermediate_count):
        self.IP_addr_end = "localhost"
        self.containers_and_load = {}
        self.containers_and_load_lock=threading.Lock()
        self.first_run = True
        self.load_balancing_type = loadType
        self.auto_scaler_type = autoScaleType
        self.round_robin_index = 0
        self.services = services
        self.intermediateCount = intermediate_count 
        print("Services: " + str(self.services))
        self.base = base
        self.start_end_server_container()
        self.count = 1
        t1=threading.Thread(target=self.run_function_every_secs_seconds,args=(5,))
        t1.start()

    def first_free_container_port(self):
        for i in range(self.base, self.base + 10):
            if str(i) not in self.containers_and_load:
                return str(i)

    def add_end_server_container(self):
        docker_client = docker.from_env()
        free = self.first_free_container_port()
        docker_client.containers.run(
            "endserversleep",
            name="endserverContainer" + free,
            detach=True,
            network="cloudtemp",
            ports={"50051/tcp": free},
        )
        with self.containers_and_load_lock:
            self.containers_and_load[free] = 0
        sleep(1)
        print("New endserver container started at " + free)
        self.round_robin_index += 1
        return free
    
    def LeAutoScaler(self):
        print("Auto scaler runs...")
        print(self.containers_and_load.copy())
        if len(self.containers_and_load) == 0 :
            return
        if self.auto_scaler_type == 1:
            logger.debug("AutoScaling via threshold base analysis")
            for key, value in self.containers_and_load.copy().items():
                containerId = "endserverContainer" + key
                cpu_usage = self.get_cpu_usage(containerId)
                print(cpu_usage)
                if len(self.containers_and_load)<10 and cpu_usage > 0.005:
                    logger.debug("Increasing instances")
                    self.add_end_server_container()
                elif cpu_usage == 0:
                    if key[len(key)-1] == '0' or key[len(key)-1] == '1':
                        continue
                    logger.debug("Decreasing instances")
                    self.removeContainer(containerId)
                    with self.containers_and_load_lock:
                        del self.containers_and_load[key]

        elif self.auto_scaler_type == 2:
            logger.debug("AutoScaling via queueing theory")
            for key, value in self.containers_and_load.copy().items(): 
                if len(self.containers_and_load)<10 and value > 5:
                    # Increase instances
                    self.add_end_server_container()
                elif value == 0:
                    # Call the processing function for values equal to 0
                    containerId = "endserverContainer" + key
                    if key[len(key)-1] == '0' or key[len(key)-1] == '1':
                        continue
                    self.removeContainer(containerId)
                    # Remove the entry from the dictionary
                    with self.containers_and_load_lock:
                        del self.containers_and_load[key]
    def run_function_every_secs_seconds(self, secs):
        while True:
            self.LeAutoScaler()
            sleep(secs);
    
    def start_end_server_container(self):
        logger.debug("Starting end server container...")
        # Docker client setup
        if self.intermediateCount == 0:
            self.removeAllContainers()
        docker_client = docker.from_env()
        logger.debug("Fetched docker env information...")

        # Check if End Server container is running, if not, start the container
        containers = docker_client.containers.list(
            all=True, filters={"name": "endserverContainer"}
        )
        # print(containers)
        logger.debug("Extracted list of containers")
        containers = None
        if not containers:
            free = self.first_free_container_port()
            docker_client.containers.run(
                "endserversleep",
                name="endserverContainer" + free,
                detach=True,
                network="cloudtemp",
                ports={"50051/tcp": free},
            )
            with self.containers_and_load_lock:
                self.containers_and_load[free] = 0
            free = self.first_free_container_port()
            docker_client.containers.run(
                "endserversleep",
                name="endserverContainer" + free,
                detach=True,
                network="cloudtemp",
                ports={"50051/tcp": free},
            )

            with self.containers_and_load_lock:
                self.containers_and_load[free] = 0
            print("Primary end server containers started.")
            logger.debug("Primary end server containers started.")
        else:
            print(
                "Primary end server containers are already running. System must be restarted."
            )
            logger.debug(
                "Primary end server containers are already running. System must be restarted."
            )
        logger.debug("Reached end of start_end_server_container()")
        # self.IP_addr_end = "endserverContainer"  # Update the IP address to the container name

    def IssueJob(self, data1, data2, function, port):
        # make grpc call based on function to localhost:port_end (later can be changed to actual IP address):
        logger.debug("Received function call for function: " + str(function))
        with grpc.insecure_channel(self.IP_addr_end + ":" + port) as channel:
            stub = trial_2_pb2_grpc.AlertStub(channel)
            if self.services[0] and function == 0:
                response = stub.RelayClientMessage(
                    trial_2_pb2.function_message(data1=data1, function=function)
                )
                logger.debug("Echoed value: " + str(response.val))

            elif self.services[1] and function == 1:
                response = stub.RelayClientMessage(
                    trial_2_pb2.function_message(
                        data1=data1,
                        data2=data2,
                        function=function,
                    )
                )
                logger.debug("Calculated simple interest value: " + str(response.val))

            elif self.services[2] and function == 2:
                response = stub.RelayClientMessage(
                    trial_2_pb2.function_message(data1=data1, function=function)
                )
                logger.debug("Computed tax value: " + str(response.val))

            elif self.services[3] and function == 3:
                response = stub.RelayClientMessage(
                    trial_2_pb2.function_message(
                        data1=data1,
                        data2=data2,
                        function=function,
                    )
                )
                logger.debug("Computed emi value: " + str(response.val))

            elif self.services[4] and function == 4:
                response = stub.RelayClientMessage(
                    trial_2_pb2.function_message(
                        data1=data1,
                        data2=data2,
                        function=function,
                    )
                )
                logger.debug("Estimated returns on FD: " + str(response.val))

            elif self.services[5] and function == 5:
                response = stub.RelayClientMessage(
                    trial_2_pb2.function_message(
                        data1=data1, data2=data2, function=function
                    )
                )
                logger.debug(
                    "Converted value in the target currency: " + str(response.val)
                )

        logger.debug("Returning value to client...")

        return trial_1_pb2.returnValue(val=response.val)

    def removeContainer(self,containerPort):
        logger.debug("removing container")
        docker_client = docker.from_env()
        container = docker_client.containers.get(containerPort)
        container.remove(force=True)
        print("Endserver container at " + containerPort + " removed")
        self.round_robin_index -= 1

    def removeAllContainers(self):
        logger.debug("Setting up server...")
        docker_client = docker.from_env()
        containers = docker_client.containers.list()
        for container in containers:
            container.remove(force=True)

    def get_cpu_usage(self,container_id):
        client = docker.from_env()
        container = client.containers.get(container_id)
        stats = container.stats(stream=False)
        # print(stats)
        return (
            100 * stats["cpu_stats"]["cpu_usage"]["total_usage"]
            / stats["cpu_stats"]["system_cpu_usage"]
            # stats["CPU %"]
        )

    def InvokeMethod(self, request, context):
        # Perform load balancing here across the end server containers that are running to determine which end server to issue the job to

        if self.load_balancing_type == 1:
            # Least connections load balancing
            selected_port = min(
                self.containers_and_load, key=self.containers_and_load.get
            )
            

        elif self.load_balancing_type == 2:
            # Random choice
            n = randint(0, len(self.containers_and_load) - 1)
            selected_port = list(self.containers_and_load.keys())[n]

        elif self.load_balancing_type == 3:
            # Power of two choices
            n1 = randint(0, len(self.containers_and_load) - 1)
            n2 = randint(0, len(self.containers_and_load) - 1)
            while n2 == n1:
                n2 = randint(0, len(self.containers_and_load) - 1)
            n1 = list(self.containers_and_load.keys())[n1]
            n2 = list(self.containers_and_load.keys())[n2]
            if self.containers_and_load[n1] <= self.containers_and_load[n2]:
                selected_port = n1
            else:
                selected_port = n2

        elif self.load_balancing_type == 4:
            # Round robin
            if self.count == 0:
                if self.round_robin_index % 2 == 0:
                    self.count = 2
                else:
                    self.count = 1

                self.round_robin_index = (self.round_robin_index + 1) % len(
                    self.containers_and_load
                )
            selected_port = list(self.containers_and_load.keys())[
                self.round_robin_index
            ]

            self.count -= 1

        elif self.load_balancing_type == 5:
            # IP hash
            octets = request.ip.split(".")
            hash_val = 0
            x = 1
            for i in octets:
                hash_val += int(i, 2) * x
                x *= 256
            selected_port = list(self.containers_and_load.keys())[
                hash_val % len(self.containers_and_load)
            ]
            # selected_port = list(self.containers_and_load.keys())[0]  # temporary

        print("Issuing job to end server container: " + selected_port)
        logger.debug("Issuing job to end server container: " + selected_port)
        with self.containers_and_load_lock:
            self.containers_and_load[selected_port] += 1
        return_val = self.IssueJob(
            request.data1,
            request.data2,
            request.function,
            selected_port,
        )
        with self.containers_and_load_lock:
            self.containers_and_load[selected_port] -= 1

        return return_val

class Initialiser(trial_1_pb2_grpc.AlertServicer):
    def __init__(self):
        self.intermediateCount = 0
        self.basePort = "6000"
        f = open("credentials.csv", "a")
        f.close()

    def CreateAccount(self, request, context):
        with open("credentials.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([request.email, request.password])
            return trial_1_pb2.void()

    def Login(self, request, context):
        with open("credentials.csv", "r") as file:
            csv_reader = csv.reader(file)
            for cred in csv_reader:
                if cred[0] == request.email:
                    if cred[1] == request.password:
                        return trial_1_pb2.returnValue(val = 0)
                    else:
                        return trial_1_pb2.returnValue(val = 1)
            return trial_1_pb2.returnValue(val = 2)
        
    def CreateInstance(self, request, context):
        if self.intermediateCount == 9:
            return trial_1_pb2.initMessage(port="-1")

        port = self.basePort + str(self.intermediateCount)

        threading.Thread(
            target=self.InitialiseServer,
            args=(
                port,
                request.loadType,
                request.autoType,
                request.services,
            ),
        ).start()

        self.intermediateCount += 1

        return trial_1_pb2.initReply(port=int(port), services=request.services, count=self.intermediateCount)

    def InitialiseServer(self, port, loadType, autoScaleType, serviceStr):
        services = [False, False, False, False, False, False]
        for c in serviceStr:
            services[int(c)] = True

        # Initialising the connector server
        logger.debug("Initialising the connector server...")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        logger.debug("Added multithreading to the connector server...")
        trial_1_pb2_grpc.add_AlertServicer_to_server(
            Server(
                loadType, autoScaleType, services, 50000 + 10 * self.intermediateCount, self.intermediateCount
            ),
            server,
        )
        logger.debug("Initialised the connector server object...")

        # Starting the server
        server.add_insecure_port("[::]:" + port)
        server.start()
        print("Server started listening on port " + port + "...")
        logger.debug("Server started listening on port " + port + "...")
        server.wait_for_termination()


def initialise():
    # Initialising the connector server
    logger.debug("Initialising the initialiser server...")
    initialiser = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logger.debug("Added multithreading to the initialiser server...")
    trial_1_pb2_grpc.add_AlertServicer_to_server(Initialiser(), initialiser)
    logger.debug("Initialised the initialiser server object...")

    port = "40040"

    # Starting the server
    initialiser.add_insecure_port("[::]:" + port)
    initialiser.start()
    print("Server started listening on port " + port + "...")
    logger.debug("Server started listening on port " + port + "...")
    initialiser.wait_for_termination()


if __name__ == "__main__":
    # Intitialising the logger
    logging.basicConfig(
        filename="scaler.log",
        format="%(asctime)s %(message)s",
        filemode="w",
    )

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logger.debug("Before intialise() call")
    initialise()
