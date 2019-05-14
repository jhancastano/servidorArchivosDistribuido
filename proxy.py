import zmq
import sys
import json



def serverList(identidad,lista):
	ident =identidad.decode('utf8')
	print(ident)
	if ident in lista:
		print('registrado')
	else:
		lista.append(ident)
		print('registrando: '+ident)

def uploadCliente(diccionario):
	dicc = {}
	for k,v in diccionarioArchivo.items():
	return dicc

def main():
	serverList1 = []
	diccArchivos = {}
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
		print(operacion)
		if (operacion=='r'):
			serverList(destino,serverList1)
		elif (operacion =='upload'):
			pass
		elif(operacion=='download'):
			pass			
		else:
			socket.send_multipart([destino, sender, msg])

if __name__ == '__main__':
	main()
