from http.client import HTTPConnection
from wsgiref.validate import validator
from multiprocessing import Process
from time import sleep

import pytest

from .utils import TEST_ADDR, TEST_PORT
from web_server.server import HttpServer


def simple_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)

    return [b'Hello World']

def test_wsgi():

	has_assertion_error = False

	try:
		def run_server_instance(application):
			server = HttpServer(TEST_ADDR, TEST_PORT, timeout=1, application=application)

			def server_callback(server, http_connection):
				server.stop()

			server.run(server_callback)

		validator_app = validator(simple_app)
		server_process = Process(target=run_server_instance, args=(validator_app,))
		server_process.start()

		connection = HTTPConnection(TEST_ADDR, TEST_PORT)
		connection.request('GET', '/')
		connection.getresponse()
		
	except AssertionError:
		has_assertion_error = True
	finally:
		server_process.terminate()

	assert has_assertion_error == False