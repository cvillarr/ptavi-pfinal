#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import os
import time
import random

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

def log (evento):
        evento = (" ").join(evento.split())
        tiempo = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        line_log = tiempo + " " + evento + "\n"
        with  open (PATH_LOG, 'a') as log_file:
            log_file.write(line_log)

class ClientHandler(ContentHandler):
    #Creamos un diccionario para cada apartado y una lista para guardar cada diccionario

    def __init__(self):
        self.server = {"name": "", "ip": "", "puerto":""}
        self.database = {"path":"", "passwdpath":""}
        self.log = {"path": ""}
        self.listafinal = []

    def startElement(self, name, attrs):
        if name == "server":
            dicc_aux = {}
            for attr in self.server:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == "database":
            dicc_aux = {}
            for attr in self.database:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])
        elif name == "log":
            dicc_aux = {}
            for attr in self.log:
                dicc_aux[attr] = attrs.get(attr, '')
            self.listafinal.append([name, dicc_aux])

    def get_tags(self):

        return self.listafinal

class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""
    def handle(self):

        line = self.rfile.read().decode('utf-8')
        line_conten = line.split()
        print("El cliente nos manda " + line)
        log("Received from " + str(self.client_address[0]) + ":" + 
            str(self.client_address[1]) + " " + line)

        if line_conten[0] == "REGISTER":
            if len(line_conten) != 4 and 6:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
            else:
                if len(line_conten) != 6:
                    nonce = str(random.randint(0, 999999999999999999999))
                self.wfile.write(b"SIP/2.0 401 Unauthorized\r\n" +
                                 b"WWW Authenticate: Digest nonce= " + b'"' +
                                 bytes(nonce, 'utf-8') + b'"')
                
        elif line_conten[0] != "BYE":
            if line_conten[0] != "ACK":
                    if line_conten[0] != "INVITE":
                        self.wfile.write(b"SIP/2.0 405 Method Not Allowed")
 
if __name__ == "__main__":

    try:
        archivo = sys.argv[1]

    except IndexError:
        sys.exit("Usage: python proxy_registrar.py config")

    parser = make_parser()
    cHandler = ClientHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(archivo))
    listafinal = cHandler.get_tags()
    print(listafinal)

    PORT_PROXY = listafinal[0][1]["puerto"]
    SERVER = listafinal[0][1]["name"]
    PATH_LOG = listafinal[2][1]["path"]
    
    log("Starting proxy...")
    
    serv = socketserver.UDPServer(('', int(PORT_PROXY)), EchoHandler)
    LINE = "Server " + SERVER + " listening at port " + PORT_PROXY
    print(LINE)
    
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Proxy finished")
        log("Finishing")