#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
import os


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
                self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        elif line_conten[0] == "REGISTER":
            if len(line_conten) != 4:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
        elif line_conten[0] == "ACK":
            aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 <' + ARCHIVO
            print("Vamos a ejecutar", aEjecutar)
            os.system(aEjecutar)
        elif line_conten[0] == "BYE":
            self.wfile.write(b"Finalizando comunicacion")
        if line_conten[0] != "BYE":
            if line_conten[0] != "ACK":
                    if line_conten[0] != "INVITE":
                        self.wfile.write(b"SIP/2.0 405 Method Not Allowed")

        # Si no hay más líneas salimos del bucle infinito


if __name__ == "__main__":
    try:
        PORT = int(sys.argv[2])
        ARCHIVO = sys.argv[3]
    # Creamos servidor de eco y escuchamos
        serv = socketserver.UDPServer(('', PORT), EchoHandler)
        print("Listening...")
        serv.serve_forever()
    except IndexError:
        sys.exit("Usage: python3 server.py IP port audio_file")
