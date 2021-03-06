#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
import os
import time

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
        self.account = {"username": "", "passwd": ""}
        self.uaserver = {"ip": "", "puerto": ""}
        self.rtpaudio = {"puerto": ""}
        self.regproxy = {"ip": "", "puerto": ""}
        self.log = {"path": ""}
        self.audio = {"path": ""}
        self.listafinal = []

    def startElement(self, name, attrs):
        """Configuro las distintas opciones que tiene el servidor."""
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
        """Devuelve la lista final de la configuración."""
        return self.listafinal


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    port_audc = "1122"

    def handle(self):
        """Manejador de códigos de respuesta del servidor final."""
        line = self.rfile.read().decode('utf-8')
        line_conten = line.split()
        print("El cliente nos manda " + line)
        log("Received from " + SERVER + ":" + PORT_PROXY + line)

        if line_conten[0] == "INVITE":
            if len(line_conten) != 13:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
                line = "SIP/2.0 400 Bad Request\r\n\r\n"
                log("Sent to " + SERVER + ":" + PORT_PROXY + line)
            else:

                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                self.wfile.write(b"SIP/2.0 180 Ring\r\n\r\n")
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n"
                                 + b"Content-Type: application/sdp\r\n\r\n"
                                 + b"v=0\r\n" + b"o=" +
                                 bytes(line_conten[6].split("=")[-1], 'utf-8')
                                 + b" " + bytes(SERVER, 'utf-8') + b"\r\n"
                                 + b"s=Misesion\r\n" + b"t=0\r\n" + b"m=audio "
                                 + bytes(self.port_audc, 'utf-8') +
                                 b" RTP\r\n")
                line = "SIP/2.0 100 Trying 180 Ring 200 OK"
                log("Sent to " + SERVER + ":" + PORT_PROXY + line)

        elif line_conten[0] == "ACK":
            media = "< cancion.mp3"
            aEjecutar = "mp32rtp -i 127.0.0.1 -p" + self.port_audc + media
            print("Vamos a ejecutar", aEjecutar)
            os.system(aEjecutar)
            self.wfile.write(b"Recibiendo archivo...\r\n\r\n")
            log("Sent to " + SERVER + ":" + PORT_PROXY + " " + line)
        elif line_conten[0] == "BYE":
            if len(line_conten) != 3:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
                line = "SIP/2.0 400 Bad Request"
                log("Sent to " + SERVER + ":" + PORT_PROXY + " " + line)
            else:
                self.wfile.write(b"SIP/2.0 200 OK Finalizando comunicacion")
                line = " Finalizando comunicación"
                log("Sent to " + SERVER + ":" + PORT_PROXY + " " + line)
        if line_conten[0] != "BYE":
            if line_conten[0] != "ACK":
                    if line_conten[0] != "INVITE":
                        self.wfile.write(b"SIP/2.0 405 Method Not Allowed")
                        line = "SIP/2.0 405 Method Not Allowed"
                        log("Sent to " + SERVER + ":" + PORT_PROXY + line)

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
    PORT_AUDIO = listafinal[2][1]["puerto"]
    PORT_PROXY = listafinal[3][1]["puerto"]
    PATH_LOG = listafinal[4][1]["path"]
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(PORT)), EchoHandler)
    print("Listening...")
    log("Starting...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Server finished")
        log("Finishing")
