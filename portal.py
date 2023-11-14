from __future__ import print_function
import logging
import grpc
import trial_1_pb2
import trial_1_pb2_grpc
import random

logging.basicConfig(
    filename="client.log", format="%(asctime)s %(message)s", filemode="w"
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# IP_addr_intermediate = "172.17.63.199"
ipInitialiser = "localhost"
portInitialiser = "40040"


def run():
    print("Select a combination of the following services: ")
    print("0. Echo")
    print("1. Simple interest calculation")
    print("2. Tax computation")
    print("3. EMI calculation")
    print("4. FD returns calculation")
    print("5. Currency conversion")

    services = input(
        "Enter a combination for services: \n Example: To choose services 1, 3, and 4, enter 134\nChoice: "
    )
    logger.debug("Tenant is requesting services: " + services)

    print("Select from the following types of load balancers: ")
    print(
        "1. Least connections \n 2. Random choice \n 3. Power of two choices \n 4. Round robin \n 5. IP hash"
    )
    loadBalancerType = int(
        input(
            "Enter load balancing type: \n Example: To choose type 1, enter 1\nChoice: "
        )
    )

    print("Select from the following types of auto-scalers: ")
    print("1. Threshold based \n 2. Queue based")
    autoScalerType = int(
        input(
            "Enter load balancing type: \n Example: To choose type 1, enter 1\nChoice: "
        )
    )

    logger.debug(
        "Tenant is requesting load balancer type: "
        + str(loadBalancerType)
        + " and auto scaler type: "
        + str(autoScalerType)
    )

    with grpc.insecure_channel(ipInitialiser + ":" + portInitialiser) as channel:
        stub = trial_1_pb2_grpc.AlertStub(channel)
        response = stub.CreateInstance(
            trial_1_pb2.initMessage(
                loadType=loadBalancerType,
                autoType=autoScalerType,
                services=services,
            )
        )
        logger.debug("Initialised intermediate's port number: " + str(response.port))
        logger.debug("Initialised services: " + response.services)
        print(
            "Initialised intermediate's port number "
            + str(response.port)
            + " and services: "
            + response.services
        )

        if response.port == "-1":
            print("No intermediate server available")
            logger.debug("No intermediate server available")
            return

        # Open file in read/write mode and add intermediate's port number as well as services in two separate lines
        with open("tenant" + str(response.count) +".txt", "w") as f:
            f.write(str(response.port) + "\n")
            f.write(response.services + "\n")
        f.close()


if __name__ == "__main__":
    run()
