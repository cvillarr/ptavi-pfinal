#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
import os

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

class ClientHandler(ContentHandler):
    #Creamos un diccionario para cada apartado y una lista para guardar cada diccionario
    def __init__(self):
        self.account = {"username": "", "passwd": ""}
        self.uaserver = {"ip": "", "puerto": ""}
        self.rtpaudio = {"puerto": ""}
        self.regproxy = {"ip": "", "puerto": ""}
        self.log = {"path": ""}
        self.audio = {"path": ""}
        self.listafinal = [] 

    def startElement(self, name, attrs):
        if name == "account":
            dicc_aux = {}
            for attr in self.account:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == "uaserver":
            dicc_aux = {}
            for attr in self.uaserver:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == "rtpaudio":
            dicc_aux = {}
            for attr in self.rtpaudio:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == "regproxy":
            dicc_aux = {}
            for attr in self.regproxy:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == "log":
            dicc_aux = {}
            for attr in self.log:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == "audio":
            dicc_aux = {}
            for attr in self.audio:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])

    def get_tags(self):
        
        return self.listafinal


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        # Leyendo línea a línea lo que nos envía el cliente
        line = self.rfile.read().decode('utf-8')
        line_conten = line.split()
        print("El cliente nos manda " + line)

        if line_conten[0] == "INVITE":
            if len(line_conten) != 13:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
            else:
                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                self.wfile.write(b"SIP/2.0 180 Ring\r\n\r\n")
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n"
                                 + b"Content-Type: application/sdp\r\n\r\n" 
                                 + b"v=0\r\n" + b"o=" 
                                 + bytes(line_conten[6].split("=")[-1], 'utf-8') 
                                 + b" " + bytes(SERVER, 'utf-8') + b"\r\n" 
                                 + b"s=Misesion\r\n" + b"t=0\r\n" + b"m=audio " 
                                 + bytes(PORT_AUDIO, 'utf-8') + b" RTP\r\n")
        elif line_conten[0] == "REGISTER":
            if len(line_conten) != 4:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
        elif line_conten[0] == "ACK":
            aEjecutar = "mp32rtp -i 127.0.0.1 -p 23032 < cancion.mp3"
            print("Vamos a ejecutar", aEjecutar)
            os.system(aEjecutar)
        elif line_conten[0] == "BYE":
            if len(line_conten) != 3:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
            else:
                self.wfile.write(b"Finalizando comunicacion")
        if line_conten[0] != "BYE":
            if line_conten[0] != "ACK":
                    if line_conten[0] != "INVITE":
                        self.wfile.write(b"SIP/2.0 405 Method Not Allowed")

        # Si no hay más líneas salimos del bucle infinito


if __name__ == "__main__":

    try:
        archivo = sys.argv[1]
    except IndexError:
        sys.exit("Usage: python3 uaserver.py config")

    parser = make_parser()
    cHandler = ClientHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(archivo))
    listafinal = cHandler.get_tags()

    PORT = listafinal[1][1]["puerto"]
    SERVER = listafinal[1][1]["ip"]
    USUARIO = listafinal[0][1]["username"]
    PORT_AUDIO = listafinal [2][1]["puerto"]
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(PORT)), EchoHandler)
    print("Listening...")
    serv.serve_forever()

