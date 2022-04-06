import socket
import threading
import sys

HEADER = 64
HOSTNAME = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOSTNAME, PORT)
DISCONNECT_MESSAGE = b"!DISCONNECT"

try:
	while True:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server.bind(ADDR)
		print("[STARTING] servers is starting...")

		server.listen(5)
		print(f"[LISTENING] Server is listening on {HOSTNAME}")

		# Allow client access
		client, addr = server.accept()
		print(f"\n [NEW CONNECTIONS] {addr} connected. \n")
		
		# Recieve message from client
		data = client.recv(HEADER).decode('utf-8')
		print(f"\n [Message from Client] : {data} \n")

		# Send message to client
		msg = "Ahoy!"
		client.send(bytes(msg, 'utf-8'))
except socket.error as msg:
	print(f"Bind failed. Error code : {str(msg[0])}, Message : {msg[1]}")
	# sys.exit()
finally:
	print("\n [Server Done!] Close Connection... \n")
	client.close()