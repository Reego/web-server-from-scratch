from http import HTTPStatus
from itertools import islice

class HttpRequest:

	def __init__(self, request):
		
		upper, body = request.split('\n\n', 1) if request.find('\n\n') >= 0 else request, ''
		upper_lines = request.split('\n')

		starting_line = upper_lines[0].split(' ')
		self.method = starting_line[0]
		self.path = starting_line[1]

		self.headers = {}

		for line in islice(upper_lines, 1, len(upper_lines) - 2):

			header_label, header_value = line.split(': ', 1)
			self.headers[header_label] = header_value

		self.body = body

class HttpResponse:

	DEFAULT_HEADERS = {}

	def __init__(self, request, headers={}, status=HTTPStatus.OK, body=''):

		self.headers = headers

		self.status = status

		self.body = body

		if self.body:
			self.headers['Content-Length'] = len(self.body)
			self.headers['Content-Type'] = 'text/html'


	def __str__(self):
		headers_text = '\n'.join([f'{key}: {value}' for key, value in self.headers.items()])

		return f"""
HTTP/1.1 {self.status.phrase} {self.status.value}
{headers_text}

{self.body}"""

	def __repr__(self):
		return str(self)

	@property
	def bytes(self):
		return str(self).encode()