import zmq
import sys
import json
import numpy
import itertools
import random
import hashlib
import os
def upload(json):
	pass

def download(json):
	pass

def hashearArchivo(FILE):
	SizeFile = os.stat(FILE).st_size
	SizePart = 1024*10
	diccionario = {}
	DicPart = {}
	FileComplete = hashlib.sha1()
	with open(FILE, 'rb') as f:
		i= 1
		for x in range(int(SizeFile/SizePart)+1):			
			data = f.read(SizePart)
			objetohash = hashlib.sha1(data)
			cadena = objetohash.hexdigest()
			DicPart.update({i:cadena})
			FileComplete.update(data)
			i=i+1
	shaprincipal =	FileComplete.hexdigest()	
	diccionario.update({shaprincipal:DicPart})
	return diccionario

def hashf(FILE):
	with open(FILE, 'rb') as f:
		data = f.read()
		objetohash = hashlib.sha1(data)
		cadena = objetohash.hexdigest()	
	print(cadena)

def comprobarHash(diccionarioArchivo):
	h = hashlib.sha1()

	for k,v in diccionarioArchivo.items():
		print(k)
		print(v)
	print('-------------------------')
	return h.hexdigest()

def main():
	print(2^4)
	dicc = {}
	identity = b'1'
	servidortcp = "tcp://localhost:4444"
	context = zmq.Context()
	socket = context.socket(zmq.DEALER)
	socket.identity = identity
	socket.connect(servidortcp)
	print("Started client with id {}".format(identity))
	poller = zmq.Poller()
	poller.register(sys.stdin, zmq.POLLIN)
	poller.register(socket, zmq.POLLIN)
	while True:
		socks = dict(poller.poll())
		mensaje = {'operacion':'sin operacion'}
		mensaje_json = json.dumps(mensaje)
		if socket in socks:
			sender, msg = socket.recv_multipart()
			mensaje_json = json.loads(msg)
			operacion = mensaje_json['operacion']
			if(operacion=='upload'):
				upload(json['arreglo'])
			elif(operacion=='download'):
				download(json['arreglo'])


			print(msg)
		elif sys.stdin.fileno() in socks:
			print("?")
			command = input()
			op, msg = command.split(' ', 1)
			mensaje = {'operacion':'upload','arreglo':{}}
			mensaje_json = json.dumps(mensaje)
			socket.send_multipart([identity,mensaje_json.encode('utf8')])


if __name__ == '__main__':
	main()
    