import logging
from concurrent import futures
import grpc
import trial_1_pb2_grpc
from time import sleep
import threading


class Server(trial_1_pb2_grpc.AlertServicer):
    def __init__(self):
        self.IP_addr_end = "localhost"
        self.containers_and_load = {}
        self.first_run = True
        self.load_balancing_type = 4
        self.round_robin_index = 0


def serve1():
    sleep(5)
    # Initialising the connector server
    logger.debug("Initialising the connector server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logger.debug("Added multithreading to the connector server...")
    trial_1_pb2_grpc.add_AlertServicer_to_server(Server(), server)
    logger.debug("Initialised the connector server object...")
    port = 50050

    # Starting the server
    server.add_insecure_port("[::]:" + str(port))
    server.start()
    print("Server started listening on port " + str(port) + "...")
    logger.debug("Server started listening on port " + str(port) + "...")
    server.wait_for_termination()


def serve2():
    # Initialising the connector server
    logger.debug("Initialising the connector server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logger.debug("Added multithreading to the connector server...")
    trial_1_pb2_grpc.add_AlertServicer_to_server(Server(), server)
    logger.debug("Initialised the connector server object...")
    port = 40040

    # Starting the server
    server.add_insecure_port("[::]:" + str(port))
    threading.Thread(target=serve1).start()
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

    serve2()
