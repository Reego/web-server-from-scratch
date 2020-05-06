import socket

from web_server.connection_handler import handle_connection

ADDR, PORT = '127.0.0.1', 5000

def main():
	sock = socket.socket()

	with socket.socket() as sock:
		sock.bind((ADDR, PORT))
		sock.listen()

		while True:

			client_connection, client = sock.accept()
			handle_connection(client_connection)
			client_connection.close()


if __name__ == '__main__':
	main()