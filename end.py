import logging
from concurrent import futures
import grpc
import trial_2_pb2
import trial_2_pb2_grpc
import service
from time import sleep


class Server(trial_2_pb2_grpc.AlertServicer):
    def __init__(self):
        self.interest_rate = 0.05
        self.emi_rate = 0.07
        self.FD_rate = 0.10
    
    def evaluate_function_1(self, data1, data2):
        return data1*self.interest_rate*data2
    
    def RelayClientMessage(self, request, context):
        logger.debug("Received request from intermediate node")
        logger.debug("Function type received: " + str(request.function))

        val = 0
        
        if request.function == 0:
            val = request.data1
        elif request.function == 1:
            val = self.evaluate_function_1(data1 = request.data1, data2 = request.data2)
        elif request.function == 2:
            val = service.taxComputation(income_rs = request.data1)
        elif request.function == 3:
            val = service.emiCalculator(loan_amount_rs = request.data1, rate_pa = self.emi_rate, tenure_yrs = request.data2)
        elif request.function == 4:
            val = service.FDReturnsCalculator(investment_rs = request.data1, rate_pa = self.FD_rate, tenure_yrs = request.data2)
        elif request.function == 5:
            val = service.currencyConverter(amount = request.data1, currency = request.data2)
        sleep(60)
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