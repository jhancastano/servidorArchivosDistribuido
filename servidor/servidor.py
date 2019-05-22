import zmq
import sys
import json
import numpy
import itertools
import random
from collections import namedtuple
import socket as sck

def get_Host_name_IP(): 
    try: 
        host_name = sck.gethostname() 
        host_ip = sck.gethostbyname(host_name) 
         
        return host_ip 
    except: 
        print("Unable to get Hostname and IP") 

def upload(msg,data):
    print(msg['name'])
    with open(msg['name'], 'wb') as f:
        f.write(data)

def download(msg):
    dicc = {}
    print(msg['name'])
    with open(msg['name'],'rb') as f:
        data = f.read()
    dicc = {'nombre':msg['name'],'data':data}    
    return dicc

def main():
    
    print('ingrese direccion IP del servidor proxy')
    direccionProxy = input()

    servidortcp = "tcp://"+direccionProxy+":4444"
    number  = random.randrange(4445,9999)

    print('ingrese direccion IP del servidor local')
    direccion = input()
    nombrework = 'tcp://'+ direccion + ':'+str(number)
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
    socketS.bind("tcp://*:"+str(number))

    print("Started server Archivos")

    while True:
        sender, destino , msg, data = socketS.recv_multipart()
        mensaje_json = json.loads(msg)
        operacion = mensaje_json['operacion']
        print(operacion)
        if (operacion=='upload'):
            upload(mensaje_json,data)
            pass
        elif(operacion=='download'):
            m = download(mensaje_json)
            mensaje = {'operacion':'download','archivo':{'nombre':m['nombre']}}
            msg=json.dumps(mensaje)
            socketS.send_multipart([destino, sender, msg.encode('utf8'),m['data']])
            pass            
        else:
            socketS.send_multipart([destino, sender, msg])



if __name__ == '__main__':
    main()