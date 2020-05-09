from .application import Application

from http import HTTPStatus

class MockApplication(Application):

	def run(self, environ):

		request_data = dict(environ)

		return f'Request for {request_data["SERVER_NAME"]}:{request_data["SERVER_PORT"]}{request_data["PATH_INFO"]}', HTTPStatus.OK