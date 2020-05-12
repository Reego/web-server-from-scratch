from .application import Application

from http import HTTPStatus

class MockApplication(Application):

	def run(self, environ):

		return f'Request for {environ["SERVER_NAME"]}:{environ["SERVER_PORT"]}{environ["PATH_INFO"]}'.encode(), HTTPStatus.OK