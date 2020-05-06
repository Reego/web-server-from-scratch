from .http_messages import HttpRequest, HttpResponse

def handle_connection(client_connection):
	"""handles the socket connection"""

	pre_parsed_request = client_connection.recv(1024)

	req = HttpRequest(pre_parsed_request.decode())


	response = HttpResponse(req, body='Hello, world!')

	print(str(response))
	client_connection.sendall(response.bytes)