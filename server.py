import socket
import sys
import select
import sqlite3
import queue
import bcrypt


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
dataBase = sqlite3.connect('users.db')
db = dataBase.cursor()

# There's going to be some TLS here, but cross that bridge once you get to it, I suppose.

# Bind socket to self
server_address = ('localhost', 10000)
print("starting up on %s port %s" % server_address) 

sock.bind(server_address)
sock.listen(5)

inputs = [ sock ]
outputs = []
messageQueues = {}

while inputs:
	# Wait for at least one of the sockets to be ready for processing
	print("\nwaiting for the next event")
	readable, writable, exceptional = select.select(inputs, outputs, inputs)

	for s in readable:
		if s is sock: 
			# this means there's a new connection
			connection, client_address = sock.accept()

			# connection.setblocking(0)
			inputs.append(connection)
			messageQueues[connection] = queue.Queue()
			connection.send(b'Hello and welcome to my server!\n')

			# preferably put all of authentication in its own function
			connection.send(b"please enter your username:\n")
			username = connection.recv(64) 
			data = b'your username was ' + bytes(username) 
			connection.send(data)

			connection.send(b"please enter your password:\n")
			password = connection.recv(64)
			connection.send(b"password recieved\n")
			# compare the password to the hash - hopefully in another function/thread
			# 
			# db.execute('SELECT Password FROM Users WHERE Username = ? ', username)
			# hashed = db.fetchone()
			#
			# if bcrypt.checkpw(password, hashed):
			# 	connection.send("user authenticated!")
			# else:
			# 	connection.send("please reconnect")
			#	inputs.remove(connection)
			#	connection.close()

		else:
			data = connection.recv(64)
			if data:
				# accept their data, put them in the output list if
				# they're not already there, and put that message 
				# in every client's message queue
				if s not in outputs:
					outputs.append(s)
				for client in messageQueues:
					messageQueues[client].put(data)
			else:
				# a readable socket with no data is an empty connection.
				# remove them both from outputs and inputs
				if s in outputs:
					outputs.remove(s)
				inputs.remove(s)
				s.close()
	# figure out how this works
	for w in writable:
		# i think the .get_nowait() just means push everything??
		try:
			nextMsg = messageQueues[w].get_nowait()
		except queue.Empty:
			print(b"output queue for ", w.getpeername(), " is empty")
			outputs.remove(w)
		else:

			for i in inputs:
				if i is not sock:
					print("sending {} to {}".format(nextMsg, i.getpeername()))
					i.send(nextMsg)

	for e in exceptional:
		print(b"handling exceptional condition for {}".format(s.getpeername()))
		inputs.remove(e)

		if e in outputs:
			outputs.remove(e)
		e.close()

		del messageQueues[e]


