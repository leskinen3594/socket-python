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
message_stack = list()

wordlist = ['laying', 'sit_on_the_floor']

def activity_counter(activities: list) -> int:
    count_laying = activities.count('laying')
    count_sit = activities.count('sit_on_the_floor')

    return count_laying, count_sit

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

		# Add message to list for count activity
		if msg in wordlist:
			message_stack.append(msg)

		activity_list = list()
		if len(message_stack) == 9_000:
			activity_list = message_stack.copy()
			message_stack.clear()

		laying, sit_on_the_floor = activity_counter(activity_list)

		# Send to line or Remove all elements
		if laying >= 5_400 or sit_on_the_floor >= 5_400:
			# Send message to line
			if laying > sit_on_the_floor:
				# _ = lineNotify(str(addr[0]) + " : laying")
				t1 = threading.Thread(target=lineNotify, args=(str(addr[0]) + " : laying",))
				t1.start()
				print("\n [Line notify!] : laying \n")
			else:
				# _ = lineNotify(str(addr[0]) + " : sit on the floor")
				t2 = threading.Thread(target=lineNotify, args=(str(addr[0]) + " : sit on the floor",))
				t2.start()
				print("\n [Line notify!] : sit on the floor \n")

			activity_list.clear()
			laying = 0
			sit_on_the_floor = 0
		else:
			if len(activity_list) == 10:
				# Reset activity count
				activity_list.clear()
				laying = 0
				sit_on_the_floor = 0

		# Ping Pong
		ping_broadcast = "!Ahoy"
		ping_server = "!ping"
		pong = "Yo-Ho! " + str(addr[0])

		if msg == ping_broadcast:
			for c in client_list:
				c.sendall(pong.encode('utf-8'))

		if msg == ping_server:
			client.send(bytes("pong!", encoding='utf-8'))

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