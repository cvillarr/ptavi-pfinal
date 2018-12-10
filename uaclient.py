#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente que abre un socket a un servidor."""
import socket
import sys

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

class ClientHandler(ContentHandler):
    #Creamos un diccionario para cada apartado
    def __init__(self):
        self.account = {"username": "", "passwd": ""}
        self.uaserver = {"ip": "", "puerto": ""}
        self.rtpaudio = {"puerto": ""}
        self.regproxy = {"ip": "", "puerto": ""}
        self.log = {"path": ""}
        self.audio = {"path": ""}
        self.listafinal = [] 

    def startElement(self, name, attrs):
        if name == 'account':
            dicc_aux = {}
            for attr in self.account:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == 'uaserver':
            dicc_aux = {}
            for attr in self.uaserver:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == 'rtpaudio':
            dicc_aux = {}
            for attr in self.rtpaudio:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == 'regproxy':
            dicc_aux = {}
            for attr in self.regproxy:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == 'log':
            dicc_aux = {}
            for attr in self.log:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == 'audio':
            dicc_aux = {}
            for attr in self.audio:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])

    def get_tags(self):
        
        return self.listafinal
        


if __name__ == "__main__":
    
    archivo = sys.argv[1]
    parser = make_parser()
    cHandler = ClientHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(archivo))
    listafinal = cHandler.get_tags()
    print(listafinal)
    
    listafinal[1][1]["puerto"]
    listafinal[1][1]["ip"]
    listafinal[0][1]["username"]
"""

try:
    CONFIG = sys.argv[1]
    METODO = sys.argv[2]
    OPCION = sys.argv[3]

    # Contenido que vamos a enviar
    LINE = (METODO + ' sip:' + USUARIO + ' SIP/2.0\r\n')

except IndexError:
    sys.exit('Usage: python3 uaclient.py config method option')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    print("Enviando: " + LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print(data.decode('utf-8'))
    if METODO == "INVITE":
        my_socket.send(bytes("ACK sip:" + USUARIO + " SIP/2.0", "utf-8")
                       + b"\r\n")
        data = my_socket.recv(1024)
        print(data.decode('utf-8'))

    print("Fin.")
"""