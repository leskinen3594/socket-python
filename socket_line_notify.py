#################################################################
#			Line Notify                             #
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
#	            SOCKET SERVER				#
#################################################################

import socket
import threading
from my_queue import MyQueue

# SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_IP = '0.0.0.0'
PORT = 5050
BUFFER_SIZE = 16

commands = dict(
	Disconnect = ("!DISCONNECT", "!Disconnect", "!disconnect"),
)

client_list = list()	# Client List


def activity_counter(activities: list) -> int:
	# print(f"\n [Debug 4] : activities = {activities} \n")
	count_laying = activities.count('laying')
	count_sit = activities.count('sit_foor')

	return count_laying, count_sit


def client_handler(client, addr):
	event_count = 0
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
		# receive message per seconds
		# detect 7 frame per 1 senconds
		# 60 s = 420 frame
		# Queue max length default = 100
		q_length = 50
		q_message = MyQueue(q_length)

		if msg is not None:
			activity_list = q_message.push_q(msg)

			if len(activity_list) >= q_length:
				event_count += 1

		# print(f"\n [Debug 1] : queue length = {len(activity_list)} \n")
		# print(f"\n [Debug 2] : event count = {event_count} \n")
		# print(f"\n [Debug 3] : queue = {activity_list} \n")

		if event_count == 35:	# 5 seconds
			laying, sit_on_the_floor = activity_counter(activity_list[15:50])	# last 35 messages

			if laying >= 24 or sit_on_the_floor >= 24:
				# Send message to line
				if laying > sit_on_the_floor:
					# _ = lineNotify(str(addr[0]) + " : laying")
					t1 = threading.Thread(target=lineNotify, args=(str(addr[0]) + " : laying",))
					t1.start()

					client.send(bytes("Send to Line Success!", encoding='utf-8'))
				else:
					# _ = lineNotify(str(addr[0]) + " : sit on the floor")
					t2 = threading.Thread(target=lineNotify, args=(str(addr[0]) + " : sit on the floor",))
					t2.start()

					client.send(bytes("Send to Line Success!", encoding='utf-8'))

				# Reset
				laying = 0
				sit_on_the_floor = 0
			event_count = 0

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
