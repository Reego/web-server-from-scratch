from http import HTTPStatus
from itertools import islice
import sys, io, struct, socket, select

from .utils import status_phrase

FILE_EXTENSION_TO_MIME = {
	'.html': 'text/html',
	'.css': 'text/css',
	'.json': 'application/json',
}

class HttpConnection:

	def __init__(self, client_connection):

		self.client_connection = client_connection

		self.http_request = self.recvall().decode()

		# parse request string

		upper, body = self.http_request.split('\n\n', 1) if self.http_request.find('\n\n') >= 0 else self.http_request, ''
		upper_lines = upper.split('\n')
		starting_line = upper_lines[0].split(' ')

		self.method = starting_line[0]
		self.path = starting_line[1]
		self.query_string = self.path.split('?')[1] if self.path.find('?') >= 0 else ''
		self.protocol = starting_line[2]

		self.request_body = body

		self.request_headers = {}
		self.http_variables = {}

		# loop through request headers

		for line in islice(upper_lines, 1, len(upper_lines) - 2):

			header_label, header_value = line.split(': ', 1)
			self.request_headers[header_label] = header_value

			if 'HTTP_' in header_label:
				self.http_variables.append((header_label), header_value)
		
		self.content = []
		self.response_headers = {}
		self.status = HTTPStatus.OK

		self.update_response_upper_text()

	def recvall(self):
		fragments = []
		while True:
			chunk = b''
			r, _, _ = select.select([self.client_connection], [], [], .1)
			if r:
				chunk = self.client_connection.recv(1024)
			else:
				break
			fragments.append(chunk)
		return b''.join(fragments)

	def set_resource(self, resource):

		self.response_headers.update(resource.associated_headers)
		self.content.append(resource.content)

	def get_environ(self, server):
		environ = {
			'wsgi.version': (1, 1),
			'wsgi.url_scheme': 'http',
			'wsgi.input': io.StringIO(self.http_request),
			'wsgi.errors': sys.stderr,
			'wsgi.multithread': False,
			'wsgi.multiprocess': False,
			'wsgi.run_once': False,
			'REQUEST_METHOD': self.method,
			'SCRIPT_NAME': '',
			'PATH_INFO': self.path,
			'QUERY_STRING': self.query_string,
			'SERVER_NAME': server.addr,
			'SERVER_PORT': str(server.port),
			'SERVER_PROTOCOL': self.protocol,
			'CONTENT_TYPE': self.request_headers.get('Content-Type', ''),
			'CONTENT_LENGTH': self.request_headers.get('Content-Length', ''),
		}

		for variable_name, variable_value in self.http_variables.items():
			environ[variable_name] = variable_value

		return environ

	def update_response_upper_text(self):
		headers_text = '\n'.join([f'{header_label}: {header_value}'] for header_label, header_value in self.response_headers)

		self.response_upper_text = f'HTTP/1.1 {status_phrase(self.status)}\n{headers_text}'	

	def send(self, body):
		http_response = f'{self.response_upper_text}\n{body}'.encode()

		self.client_connection.sendall(http_response)