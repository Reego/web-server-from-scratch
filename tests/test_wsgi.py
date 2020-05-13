from http.client import HTTPConnection
from multiprocessing import Process
from time import sleep

import pytest

from .utils import TEST_ADDR, TEST_PORT
from web_server.server import HttpServer, ServerInterrupt


def simple_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)

    return [b'Hello World']

def server_callback(server, http_connection):
	raise ServerInterrupt()

def run_server_instance():
	from wsgiref.validate import validator
	validator_app = validator(simple_app)
	server = HttpServer(TEST_ADDR, TEST_PORT, timeout=1, application=validator_app)

	server.run(server_callback)
	print('running')

def test_wsgi():

	has_assertion_error = False

	try:
		server_process = Process(target=run_server_instance)
		server_process.start()
		print('huh')

		connection = HTTPConnection(TEST_ADDR, TEST_PORT)
		connection.request('GET', '/')
		connection.getresponse()
		
	except AssertionError:
		has_assertion_error = True
	finally:
		server_process.terminate()

	assert has_assertion_error == False