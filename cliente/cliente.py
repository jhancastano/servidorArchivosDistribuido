import zmq
import sys
import json
import numpy
import itertools
import random


import hashlib
import os


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
	dicc = {}
	dicc.update(hashearArchivo('pruebaupload.png'))
	print(comprobarHash(dicc))

if __name__ == '__main__':
	main()
    