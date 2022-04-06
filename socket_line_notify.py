#################################################################
#						Line Notify								#
#################################################################

def lineNotify(message):
	payload = {'message': message}

	return _lineNotify(payload)

def _lineNotify(payload, file=None):
	import requests

	url = 'https://notify-api.line.me/api/notify'
	token = '<Line Notify Token>'
	headers = {'Authorization': 'Bearer '+token}

	return requests.post(url, headers=headers, data=payload, files=file)


#################################################################
#						SOCKET SERVER							#
#################################################################

import socket
import threading

# SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_IP = '192.168.1.40'
PORT = 5050
BUFFER_SIZE = 4096

commands = dict(
	Disconnect = ("!DISCONNECT", "!Disconnect", "!disconnect"),
)

client_list = list()	# Client List

wordlist = ['laying', 'sit_on_the_floor']


def client_handler(client, addr):
	while True:
		try:
			data = client.recv(BUFFER_SIZE)
		except:
			client_list.remove(client)
			break

		if (not data) or (data.decode('utf-8') in commands['Disconnect']):
			client_list.remove(client)
			print(f"\n [CLIENT OUT] : {addr[0]}. \n")
			break

		msg = data.decode('utf-8')
		print(f"\n [Message from {addr[0]}] : {msg} \n")

		# Ping Pong
		ping_broadcast = "!Ahoy"
		ping_server = "!ping"
		pong = "Yo-Ho! " + str(addr[0])

		if msg == ping_broadcast:
			for c in client_list:
				c.sendall(pong.encode('utf-8'))

		if msg == ping_server:
			client.send(pong.encode('utf-8'))

		# Send message to Line
		if msg in wordlist:
			lineNotify(msg)
			# print(response)
			
	# Close conection
	client.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((SERVER_IP, PORT))
print("[STARTING] servers is starting...")

server.listen(5)
print(f"[LISTENING] Server is listening on {SERVER_IP}:{PORT}")

while True:
	client, addr = server.accept()
	client_list.append(client)
	print(f"\n [NEW CONNECTIONS] {addr} connected. \n")

	# Start threding clinet_handler
	task = threading.Thread(target=client_handler, args=(client, addr))
	task.start()