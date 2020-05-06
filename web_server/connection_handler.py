import os
from http import HTTPStatus

from .http_messages import HttpRequest, HttpResponse

PUBLIC_FOLDER = 'public'

def handle_connection(client_connection):
	"""handles the socket connection"""

	pre_parsed_request = client_connection.recv(1024)

	req = HttpRequest(pre_parsed_request.decode())

	body, status = try_get_resource(req.path)

	response = HttpResponse(req, body=body, status=status)

	client_connection.sendall(response.bytes)

def try_get_resource(path):
	"""retrieves the resource associated with the path"""
	"""returns a string, HTTPStatus tuple"""

	body = ''
	status = HTTPStatus.OK

	relative_path = path[1:]
	final_rel_path = os.path.join(PUBLIC_FOLDER, relative_path)

	final_abs_path = os.path.join(
			os.getcwd(),
			final_rel_path
	)

	if not os.path.isdir(final_abs_path) and os.path.exists(final_abs_path):
		with open(final_rel_path) as f:
			return f.read(), status

	print(f'404 at {final_rel_path}')
	return '404: File not found', HTTPStatus.NOT_FOUND