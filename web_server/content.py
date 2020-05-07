FILE_EXTENSION_TO_MIME = {
	'.html': 'text/html',
	'.css': 'text/css',
	'.json': 'application/json',
}

class HttpContent:
	"""Container for HTTP response content"""

	def __init__(self, body='', ext=None):

		self.body = body
		self.mime = FILE_EXTENSION_TO_MIME.get(ext, None)
		self.content_length = len(self.body)

	def get_headers(self):
		return {
			'Content-Type': self.mime,
			'Content-Length': self.content_length,
		}