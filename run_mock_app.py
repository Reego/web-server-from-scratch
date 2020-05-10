import socket

from web_server.server import HttpServer
from application.mock_application import MockApplication

ADDR, PORT = '127.0.0.1', 5000

if __name__ == '__main__':

	app = MockApplication.create_app()

	server = HttpServer(ADDR, PORT, application=app)
	server.run()