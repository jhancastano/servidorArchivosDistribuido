import zmq
import sys
import json
import random



def serverList(identidad,lista):
	ident =identidad.decode('utf8')
	print(ident)
	if ident in lista:
		print('registrado')
	else:
		lista.append(ident)
		print('registrando: '+ident)

def uploadCliente(diccionario,lista):
	dicc = {}
	diccionario['operacion'] = 'upload'
	nameHashComplete = diccionario['lista'].keys()
	for keys in nameHashComplete:
		name= keys	
	for k,v in diccionario['lista'][name].items():
		diccionario['lista'][name][k].update({'servidor':random.choice(lista)})
		#print(diccionario['lista'][name][k])
		pass
	dicc.update(diccionario)
	#print(diccionario)
	return dicc

def downloadCliente(msg,Diccionario):
	if msg['name']in Diccionario:
		dicc = Diccionario[msg['name']]
		print(msg['name'])
		return dicc
	else:
		return -1


def main():
	serverList1 = []
	diccArchivos = {}
	if len(sys.argv) != 1:
		print("Must be called with no arguments")
		exit()

	context = zmq.Context()
	socket = context.socket(zmq.ROUTER)
	socket.bind("tcp://*:4444")

	print("Started Proxy server")

	while True:
		sender, destino , msg = socket.recv_multipart()
		mensaje_json = json.loads(msg)
		operacion = mensaje_json['operacion']
		print(operacion)
		if (operacion=='r'):
			serverList(destino,serverList1)
		elif (operacion =='upload'):
			mensaje_json = uploadCliente(mensaje_json,serverList1)
			msg=json.dumps(mensaje_json)
			diccArchivos.update(mensaje_json['lista'])
			socket.send_multipart([destino, sender, msg.encode('utf8')])
			
		elif(operacion=='download'):
			if (downloadCliente(mensaje_json,diccArchivos)!=-1):
				msg=downloadCliente(mensaje_json,diccArchivos)
				mensaje = {'operacion':'download','nombreHash':mensaje_json['name'],'name':msg}
				msg=json.dumps(mensaje)
				socket.send_multipart([destino, sender, msg.encode('utf8')])
			else:
				print('no existe archivo')
		elif(operacion=='listar'):
			mensaje = {'operacion':'listar','list':diccArchivos}
			msg = json.dumps(mensaje)
			socket.send_multipart([destino, sender, msg.encode('utf8')])
			#print(diccArchivos)			
		else:
			socket.send_multipart([destino, sender, msg])

if __name__ == '__main__':
	main()
