def handle_connection(client_connection):
	"""handles the socket connection"""
	request = client_connection.recv(1024)
	print(request.decode())

	http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
	client_connection.sendall(http_response)