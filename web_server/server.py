import os
import socket
from http import HTTPStatus
from itertools import islice
from pathlib import Path

from .http_messages import HttpRequest, HttpResponse
from .content import HttpContent

ADDR, PORT = '127.0.0.1', 5000
PUBLIC_FOLDER_REL_PATH = './public'

class HttpServer:

	def __init__(self, addr='127.0.0.1', port=8000):
		self.addr = addr
		self.port = port
		self.sock = None

	def start(self):
		"""Starts the server"""

		self.sock = socket.socket()
		self.sock.bind((ADDR, PORT))
		self.sock.listen()

		while self.sock:
			client_connection, client = self.sock.accept()
			self.handle_connection(client_connection)
			client_connection.close()

	def stop(self):
		if self.sock:
			self.sock.close()
			self.sock = None

	def handle_connection(self, client_connection):
		"""handles the socket connection"""

		pre_parsed_request = client_connection.recv(1024)

		req = HttpRequest(pre_parsed_request.decode())
		content, status = self.try_get_resource(req.path)

		response = HttpResponse(req, content, status=status)

		client_connection.sendall(response.bytes)

	def try_get_resource(self, requested_path):
		"""retrieves the resource associated with the path"""
		"""returns a string, HTTPStatus tuple"""

		body = ''
		status = HTTPStatus.OK

		base_dir = Path(PUBLIC_FOLDER_REL_PATH)
		target_path = base_dir / Path(requested_path[1:] if requested_path != '/' else '/index.html')
		target_path.resolve()

		if base_dir in target_path.parents:
			if target_path.suffix == '':
				target_path = target_path.with_suffix('.html')

			if target_path.is_file():
				with target_path.open() as f:
					return (HttpContent(f.read(), target_path.suffix), status)

			return (HttpContent(''), HTTPStatus.NOT_FOUND)

		return (HttpContent(''), HTTPStatus.INTERNAL_SERVER_ERROR)