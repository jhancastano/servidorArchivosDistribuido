import zmq
import sys
import json
import numpy
import itertools
import time
import random
from collections import namedtuple



def main():
    servidortcp = "tcp://localhost:4444"
    number  = random.randrange(0,9999)
    nombrework = 'servidor'+ str(number)
    identity = nombrework.encode('utf8')
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.identity = identity
    socket.connect(servidortcp)
    print("Started client with id {}".format(identity))
    poller = zmq.Poller()
    poller.register(sys.stdin, zmq.POLLIN)
    poller.register(socket, zmq.POLLIN)
    #registrando worker------------ 
    rWorker = {'operacion':'registrar'}
    rWorker_json = json.dumps(rWorker)
    socket.send_multipart([identity,rWorker_json.encode('utf8')])
    #--------------------------------



if __name__ == '__main__':
    main()