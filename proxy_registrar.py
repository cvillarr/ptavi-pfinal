#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Programa proxy que hace de intermediario entre cliente y servidor."""

import socket
import socketserver
import sys
import time
import random

from xml.sax import make_parser
from xml.sax.handler import ContentHandler


def log(evento):
    """Crea un archivo para escribir los mensajes de depuración."""
    evento = (" ").join(evento.split())
    tiempo = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    line_log = tiempo + " " + evento + "\n"
    with open(PATH_LOG, 'a') as log_file:
        log_file.write(line_log)


class ClientHandler(ContentHandler):
    """Echo client class."""

    def __init__(self):
        """Crea un dicc para cada apartado y una lista para guardarlo."""
        self.server = {"name": "", "ip": "", "puerto": ""}
        self.database = {"path": "", "passwdpath": ""}
        self.log = {"path": ""}
        self.listafinal = []

    def startElement(self, name, attrs):
        """Configuro las distintas opciones que tiene el servidor proxy."""
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
        """Devuelve la lista final de la configuración."""
        return self.listafinal


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    listadatos = []

    def handle(self):
        """Manejador de códigos de respuesta del servidor proxy."""
        line = self.rfile.read().decode('utf-8')
        line_conten = line.split()
        print("El cliente nos manda " + line)
        log("Received from " + str(self.client_address[0]) + ":" +
            str(self.client_address[1]) + " " + line)

        if line_conten[0] == "REGISTER":
            if len(line_conten) != 4:
                if len(line_conten) != 7:
                    self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
                    line = "SIP/2.0 400 Bad Request\r\n\r\n"
                    log("Send to " + str(self.client_address[0]) + ":" +
                        str(self.client_address[1]) + " " + line)
                else:
                    self.wfile.write(b"REGISTRADO")
                    line = " REGISTRADO"
                    log("Send to " + str(self.client_address[0]) + ":" +
                        str(self.client_address[1]) + " " + line)

                    usuario = line_conten[1].split(":")[1]
                    ip = IP
                    puerto = line_conten[1].split(":")[-1]
                    fecha = time.strftime("%Y%m%d%H%M%S",
                                          time.localtime(time.time()))
                    expires = line_conten[3].split(":")[-1]

                    datosusuarios = {"usuario": usuario, "ip": ip,
                                     "puerto": puerto, "fecha": fecha,
                                     "expires": expires}
                    self.listadatos.append([datosusuarios])
                    with open("./listadatos.txt", 'a') as ficherodatos:
                        ficherodatos.write(str(datosusuarios))

                    print("USUARIO REGISTRADO")

            else:
                if len(line_conten) != 7:
                    nonce = str(random.randint(0, 999999999999999999999))
                    self.wfile.write(b"SIP/2.0 401 Unauthorized\r\n" +
                                     b"WWW Authenticate: Digest nonce= " + b'"'
                                     + bytes(nonce, 'utf-8') + b'"')
                    line = "SIP/2.0 401 Unauthorized WWW Authenticate:Digest nonce="
                    log("Send to " + str(self.client_address[0]) + ":" +
                        str(self.client_address[1]) + " " + line + nonce)

        elif line_conten[0] == "INVITE":
            if len(self.listadatos) >= 2:
                        PORT_ENVIO = self.listadatos[1][0]["puerto"]
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
                my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                my_socket.connect((IP, int(PORT_ENVIO)))
                my_socket.send(bytes(line, 'utf-8') + b"\r\n")
                log("Send to " + IP + ":" + PORT_ENVIO + " " + line)
                data = my_socket.recv(1024)
                line_received = data.decode('utf-8')
                log("Received from " + IP + ":" + PORT_ENVIO + " " + line)
                print(line_received)
            self.wfile.write(bytes(line_received, 'utf-8'))

        elif line_conten[0] == "ACK":
            if len(self.listadatos) >= 2:
                        PORT_ENVIO = self.listadatos[1][0]["puerto"]
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
                my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                my_socket.connect((IP, int(PORT_ENVIO)))
                my_socket.send(bytes(line, 'utf-8') + b"\r\n")
                log("Send to " + IP + ":" + PORT_ENVIO + " " + line)
                data = my_socket.recv(1024)
                line_received = data.decode('utf-8')
                log("Received from " + IP + ":" + PORT_ENVIO + " " + line)
                print(line_received)
            self.wfile.write(bytes(line_received, 'utf-8'))

        elif line_conten[0] == "BYE":
            if len(self.listadatos) >= 2:
                        PORT_ENVIO = self.listadatos[1][0]["puerto"]
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
                my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                my_socket.connect((IP, int(PORT_ENVIO)))
                my_socket.send(bytes(line, 'utf-8') + b"\r\n")
                log("Send to " + IP + ":" + PORT_ENVIO + " " + line)
                data = my_socket.recv(1024)
                line_received = data.decode('utf-8')
                log("Received from " + IP + ":" + PORT_ENVIO + " " + line)
                print(line_received)
            self.wfile.write(bytes(line_received, 'utf-8'))

        elif line_conten[0] != "BYE":
            if line_conten[0] != "ACK":
                    if line_conten[0] != "INVITE":
                        if line_conten[0] != "REGISTER":
                            self.wfile.write(b"SIP/2.0 405 Method Not Allowed")
                            line = "SIP/2.0 405 Method Not Allowed"
                            log("Send to " + str(self.client_address[0]) + ":"
                                + str(self.client_address[1]) + " " + line)


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

    IP = listafinal[0][1]["ip"]
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
