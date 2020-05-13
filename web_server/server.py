import os, sys, traceback
import socket, multiprocessing
from http import HTTPStatus
from pathlib import Path
import signal

from .http_connection import HttpConnection
from .resource import HttpResource

ADDR, PORT = '127.0.0.1', 5000


def init_worker():
	signal.signal(signal.SIGINT, signal.SIG_IGN)

class ServerInterrupt(Exception):
	pass

class HttpServer:

	def __init__(self, addr=ADDR, port=PORT, public_folder_path='/', timeout=5000, application=None):
		self.addr = addr
		self.port = port
		self.public_folder_path = public_folder_path
		self.sock = None
		self.timeout = timeout
		self.application = application

	def run(self, callback=None):
		"""Starts the server"""

		self.sock = socket.socket()
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.addr, self.port))
		# self.sock.settimeout()
		self.sock.listen()

		print(f'HTTP Server listening on {self.addr}:{self.port}...')

		pool = multiprocessing.Pool(4, init_worker)
		try:
			while self.sock is not None:
				client_connection, client = self.sock.accept()
				print('before accept')
				output = pool.apply(self.run_once, args=(client_connection,))
				if output:
					print(output)
				if callback:
					callback(self, http_connection)
		except AssertionError:
			traceback.print_exc(file=sys.stdout)
			pool.terminate()
			pool.join()
			self.stop()
			raise assertion_error
		except (KeyboardInterrupt, ServerInterrupt):
			pass
		finally:
			pool.terminate()
			pool.close()
			pool.join()
			self.stop()
		
		print('\n\nStopping HTTP Server...')
		sys.exit(0)

	def run_once(self, client_connection):
		try:
			http_connection = self.handle_connection(client_connection)

			client_connection.shutdown(socket.SHUT_WR)
			client_connection.close()
		except BaseException as error:
			return f'{type(error)}: {error}'

	def stop(self):
		self.sock.close()
		self.sock = None
		
	# called in pool
	def handle_connection(self, client_connection):
		"""handles the socket connection"""

		http_connection = HttpConnection(client_connection)

		# to maintain reference to http_connection

		def start_response(status, response_headers, exc_info=None):
			http_connection.status = status
			http_connection.response_headers.update(response_headers)
			return lambda body_data: self.send_response(http_connection, body_data)

		if self.application:
			http_connection.content.extend(self.application(http_connection.get_environ(self), start_response))
		else:
			resource, is_requested_resource = HttpResource.get_resource(self.public_folder_path, http_connection.path)
			if not is_requested_resource:
				http_connection.status = HTTPStatus.NOT_FOUND
			http_connection.set_resource(resource)
			start_response(http_connection.status, http_connection.response_headers)

		# loop through body segments and send them to the client

		for body_segment in http_connection.content:
			self.send_response(http_connection, body_segment)

		return http_connection

	def send_response(self, http_connection, body):

		# no response should be sent if the body is empty

		if not body:
			return

		http_connection.send(body)