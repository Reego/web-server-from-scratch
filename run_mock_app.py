import socket

from web_server.server import HttpServer
from application.mock_application import MockApplication

ADDR, PORT = '127.0.0.1', 5000
PUBLIC_FOLDER_REL_PATH = './public'

if __name__ == '__main__':

	app = MockApplication.create_app()

	server = HttpServer(ADDR, PORT, PUBLIC_FOLDER_REL_PATH, application=app)
	server.run()