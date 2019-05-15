import zmq
import sys
import json
import numpy
import itertools
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
    regServidor = {'operacion':'r'}
    msg = json.dumps(regServidor)
    print(msg)
    socket.send_multipart([identity,msg.encode('utf8')])
    #--------------------------------
    contextS = zmq.Context()
    socketS = context.socket(zmq.ROUTER)
    socketS.bind("tcp://*:4441")

    print("Started server Archivos")

    while True:
        sender, destino , msg = socketS.recv_multipart()
        mensaje_json = json.loads(msg)
        operacion = mensaje_json['operacion']
        print(operacion)
        if (operacion=='upload'):
            pass
        elif(operacion=='download'):
            pass            
        else:
            socketS.send_multipart([destino, sender, msg])



if __name__ == '__main__':
    main()