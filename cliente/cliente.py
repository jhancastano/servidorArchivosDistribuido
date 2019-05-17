import zmq
import sys
import json
import numpy
import itertools
import random
import hashlib
import os
import time

def joinFiles(msg,nombre):
	with open(nombre,'wb') as file:
		for x in msg['name']:
			name = msg['name'][x]['namePart']
			with open(name, 'rb') as f:
				data = f.read()
			os.remove(name)	
			file.write(data)

def upload(msg,identity):
	name = msg.keys()
	for keys in name:
		name= keys
	for x in msg[name]:
		print(msg[name][x]['servidor'])
		print(msg[name][x]['namePart'])		
		context = zmq.Context()
		socket = context.socket(zmq.DEALER)
		socket.identity = identity
		socket.connect(msg[name][x]['servidor'])
		op = 'upload'
		with open(msg[name][x]['namePart'], 'rb') as archivo:
			data = archivo.read()
			
		mensaje = {'operacion':op,'name':msg[name][x]['namePart']}
		mensaje_json = json.dumps(mensaje)
		socket.send_multipart([identity,mensaje_json.encode('utf8'),data])
		time.sleep(1)
		os.remove(msg[name][x]['namePart'])
	

def download(msg,identity):
	
	for x in msg['name']:
		context = zmq.Context()
		socket = context.socket(zmq.DEALER)
		socket.identity = identity
		socket.connect(msg['name'][x]['servidor'])
		op = 'download'
		name = msg['name'][x]['namePart']
		mensaje = {'operacion':op,'name':name}
		mensaje_json = json.dumps(mensaje)
		socket.send_multipart([identity,mensaje_json.encode('utf8'),b'datos'])

		sender, mensaje,data = socket.recv_multipart()
		time.sleep(1)
		mensaje_json = json.loads(mensaje)
		#operacion = mensaje_json['operacion']
		print(mensaje_json['archivo']['nombre'])
		print('-------')
		with open(mensaje_json['archivo']['nombre'], 'wb') as f:
			f.write(data)
	
	joinFiles(msg,'holamundo.png')	

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
			DicPart.update({i:{'namePart':cadena}})
			FileComplete.update(data)
			with open(cadena, 'wb') as part:
				part.write(data)
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
				#print(mensaje_json['lista'])
				upload(mensaje_json['lista'],identity)
			elif(operacion=='download'):
				download(mensaje_json,identity)

		elif sys.stdin.fileno() in socks:
			print("opciones[u:upload,d:download Narchivo]")
			command = input()
			op, msg = command.split(' ', 1)
			if(op=='u'):
				mensaje = {'operacion':'upload','lista':hashearArchivo('pruebaupload.png')}
				mensaje_json = json.dumps(mensaje)
			elif(op=='d'):
				mensaje = {'operacion':'download','name':'aae5ae766cd09d09ff4fc98cc118d4a8c7bda4ff'}
				mensaje_json = json.dumps(mensaje)
			else:
				pass
			socket.send_multipart([identity,mensaje_json.encode('utf8')])

if __name__ == '__main__':
	main()
    