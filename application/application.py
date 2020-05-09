from http import HTTPStatus

from web_server.utils import status_phrase

class Application():

	@classmethod
	def create_app(cls, *args, **kwargs):
		app = object.__new__(cls, *args, **kwargs)
		return app

	def __call__(self, environ, start_response):
		
		content, status = self.run(environ)
		response_headers = {}
		start_response(status, response_headers)

		return [content]

	def run(self, environ):
		return 'Hello, World!', HTTPStatus.OK