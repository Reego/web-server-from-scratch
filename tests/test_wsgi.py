from http.client import HTTPConnection
from multiprocessing import Process
from time import sleep
import sys

import pytest

from .utils import TEST_ADDR, TEST_PORT, TEST_TEXT
from web_server.server import HttpServer, ServerInterrupt

def simple_app(environm, start_response):
	status = '200 OK'
	headers = [('Content-type', 'text/plain')]
	start_response(status, headers)

	return [TEST_TEXT.encode()]

def exit_server(self, val):
	raise ServerInterrupt()

def validator_simple_app(environ, start_response):
	from wsgiref.validate import validator

	validator_wrapped_app = validator(simple_app)

	return validator_wrapped_app(environ, start_response)

def server_callback(server, output):
	raise ServerInterrupt()

def run_server_instance():
	server = HttpServer(TEST_ADDR, TEST_PORT, timeout=1, application=validator_simple_app)
	server.run(server_callback)

def test_wsgi():

	has_assertion_error = False

	try:
		server_process = Process(target=run_server_instance)
		server_process.start()

		connection = HTTPConnection(TEST_ADDR, TEST_PORT)
		connection.request('GET', '/')
		assert connection.getresponse().read() == TEST_TEXT.encode()

		sleep(.1)
		
	except AssertionError as error:
		print(error)
		has_assertion_error = True
	finally:
		server_process.terminate()

	assert has_assertion_error == False