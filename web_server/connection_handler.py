import os
from pathlib import Path
from http import HTTPStatus

from .http_messages import HttpRequest, HttpResponse
from .content import HttpContent

PUBLIC_FOLDER_REL_PATH = './public'

def handle_connection(client_connection):
	"""handles the socket connection"""

	pre_parsed_request = client_connection.recv(1024)

	req = HttpRequest(pre_parsed_request.decode())

	content, status = try_get_resource(req.path)

	response = HttpResponse(req, content=content, status=status)

	client_connection.sendall(response.bytes)

def try_get_resource(requested_path):
	"""retrieves the resource associated with the path"""
	"""returns a string, HTTPStatus tuple"""

	body = ''
	status = HTTPStatus.OK

	base_dir = Path(PUBLIC_FOLDER_REL_PATH)
	target_path = base_dir / Path(requested_path[1:])
	target_path.resolve()

	if target_path in base_dir:
		if target_path.suffix == '':
			target_path = target_path.with_suffix('.html')

		if target_path.is_file:
			with target_path.open() as f:
				return HttpContent(f.read(), target_path.suffix), status

		return HttpContent('404: File not found'), HTTPStatus.NOT_FOUND

	return HttpContent('500: Something went wrong...'), HTTPStatus.INTERNAL