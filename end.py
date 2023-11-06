import logging
import math
from concurrent import futures
import grpc
import trial_2_pb2
import trial_2_pb2_grpc



class Server(trial_2_pb2_grpc.AlertServicer):
    def __init__(self):
        self.rate = 0.05
    
    def evaluate_function_0(self, data1):
        return math.factorial(data1) * 1.00
    
    def evaluate_function_1(self, data1, data2):
        return data1*self.rate*data2
    
    def RelayClientMessage(self, request, context):
        logger.debug("Received request from intermediate node")
        logger.debug("Function type received: " + str(request.function))

        val = 0
        
        if(request.function == 0):
            val = self.evaluate_function_0(data1 = request.data1)
        else:
            val = self.evaluate_function_1(data1 = request.data1, data2 = request.data2)

        return trial_2_pb2.returnValue(val = val)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    trial_2_pb2_grpc.add_AlertServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started listening on port 50051")
    server.wait_for_termination()
    
if __name__ == "__main__":
    logging.basicConfig(filename="end.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    serve()