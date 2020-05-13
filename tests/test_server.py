from http.client import HTTPConnection

import pytest

from .utils import TEST_TEXT, TEST_FILE, TEST_ADDR, TEST_PORT, temp_resources, server_instance

def test_server(temp_resources, server_instance):

	connection = HTTPConnection(TEST_ADDR, TEST_PORT)
	connection.request('GET', '/' + TEST_FILE)

	res = connection.getresponse()
	res_body = res.read().decode()

	assert res_body == TEST_TEXT