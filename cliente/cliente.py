import zmq
import sys
import json
import numpy
import itertools
import random


import hashlib
import os


def hashearArchivo(FILE):
	diccionarioArchivo = {}
	with open(FILE, 'rb') as f:
		i= 1
		for x in f:
			data = f.read(10)
			objetohash = hashlib.sha1(data)
			cadena = objetohash.hexdigest()
			diccionarioArchivo.update({i:cadena})
			i=i+1
	return diccionarioArchivo

def hashf(FILE):
	with open(FILE, 'rb') as f:
		data = f.read()
		objetohash = hashlib.sha1(data)
		cadena = objetohash.hexdigest()	
	print(cadena)



def comprobarHash(diccionarioArchivo):
	h = hashlib.sha1()
	for k,v in diccionarioArchivo.items():
		print(v)
		h.update(v.encode('utf8'))
	print('-------------------------')
	return h.hexdigest()

def main():
	dicc = {}
	dicc.update(hashearArchivo('pruebaupload.png'))
	print('-------------------------')
	print(comprobarHash(dicc))
	print('-------------------------')
	hashf('pruebaupload.png')

if __name__ == '__main__':
	main()
    