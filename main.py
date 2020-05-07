import socket

from web_server.server import HttpServer

ADDR, PORT = '127.0.0.1', 5000

if __name__ == '__main__':
	server = HttpServer(ADDR, PORT)
	server.start()