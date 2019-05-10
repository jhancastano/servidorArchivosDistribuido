import zmq
import zmq
import sys
import json



def serverList(identidad,lista):
	ident =identidad.decode('utf8')
	if ident in lista:
		print('registrado')
	else:
		lista.append(ident)

def main():
	serverList1 = []

	if len(sys.argv) != 1:
		print("Must be called with no arguments")
		exit()

	context = zmq.Context()
	socket = context.socket(zmq.ROUTER)
	socket.bind("tcp://*:4444")

	print("Started server")

	while True:
		sender, destino , msg = socket.recv_multipart()
		mensaje_json = json.loads(msg)
		operacion = mensaje_json['operacion']
		if operacion=='registrar':
			serverList(sender,serverList1)
			print(serverList1)
		else:
			socket.send_multipart([destino, sender, msg])

if __name__ == '__main__':
	main()
