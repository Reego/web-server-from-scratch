import os
import socket
from http import HTTPStatus
from pathlib import Path

from .http_connection import HttpConnection
from .resource import HttpResource

ADDR, PORT = '127.0.0.1', 5000
PUBLIC_FOLDER_REL_PATH = './public'

class HttpServer:

	def __init__(self, addr='127.0.0.1', port=8000, timeout=5000, application=None):
		self.addr = addr
		self.port = port
		self.sock = None
		self.timeout = timeout
		self.application = application

	def start(self):
		"""Starts the server"""

		self.sock = socket.socket()
		self.sock.bind((ADDR, PORT))
		self.sock.listen(self.timeout)

		while self.sock:
			client_connection, client = self.sock.accept()
			self.handle_connection(client_connection)
			client_connection.close()

	def stop(self):
		if self.sock:
			self.sock.close()
			self.sock = None

	# called in pool
	def handle_connection(self, client_connection):
		"""handles the socket connection"""

		http_connection = HttpConnection(client_connection, self)

		# to maintain reference to http_connection

		def start_response(status, response_headers, exc_info=None):
			http_connection.status = status
			http_connection.response_headers.update(response_headers)
			return lambda body_data: self.send_response(http_connection, body_data)

		if self.application:
			http_connection.set_response_content(self.application(http_connection.environ, start_response))
		else:
			resource, is_requested_resource = HttpResource.get_resource(PUBLIC_FOLDER_REL_PATH, http_connection.path)
			if not is_requested_resource:
				http_connection.status = HTTPStatus.NOT_FOUND
			http_connection.set_resource(resource)
			start_response(http_connection.status, http_connection.response_headers)

		# loop through body segments and send them to the client

		for body_segment in http_connection.content:
			self.send_response(http_connection, body_segment)

	def send_response(self, http_connection, body):

		# no response should be sent if the body is empty

		if not body:
			return

		http_connection.send(body)