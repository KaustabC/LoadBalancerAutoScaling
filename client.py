from __future__ import print_function
import logging
import grpc
import trial_1_pb2
import trial_1_pb2_grpc
import random



logging.basicConfig(filename="client.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def run():
    function = random.randint(0, 1)
    logger.debug("Client is requesting function: " + str(function))
    if function == 0:
        logger.debug("Sending value: 4")     
        with grpc.insecure_channel("localhost:50050") as channel:
            stub = trial_1_pb2_grpc.AlertStub(channel)
            response = stub.InvokeMethod(trial_1_pb2.function_message(data1=4, function=function))
            logger.debug("Factorial value: " + str(response.val))
    else:
        logger.debug("Sending values: 1, 2")
        with grpc.insecure_channel("localhost:50050") as channel:
            stub = trial_1_pb2_grpc.AlertStub(channel)
            response = stub.InvokeMethod(trial_1_pb2.function_message(data1=4, data2=2, function=function))
            logger.debug("Simple interest: " + str(response.val))


if __name__ == "__main__":
    run()