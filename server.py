import socket
import sys
import select
import sqlite3
import queue
import bcrypt

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
			#this means there's a new connection

			connection, client_address = sock.accept()
			# connection.setblocking(0)
			
			# if usercheck(db, connection) is True:
			inputs.append(connection)
			messageQueues[connection] = Queue.Queue()
			connection.send('Hello and welcome to my server!\n')
			connection.send('Please enter your username. \n>')
			
			#preferably put all of authentication in its own function
			connection.send("please enter your username:\n")
			username = connection.recv(64)
			data = 'your username was ' + username
			connection.send(data)

			connection.send("please enter your password:\n")
			password = connection.recv(64)
			connection.send("password recieved")

			# hash the password and store it in the database - hopefully in another function/thread
			
			#
			# db.execute('SELECT Password FROM Users WHERE Username = ? ', hashed)
			# hashed = db.fetchone()
			# if bcrypt.checkpw(password, hashed):
			# 	connection.send("user authenticated!")
			# else:
			# 	connection.send("please reconnect")
			#	inputs.remove(connection)
			#	connection.close

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

	for w in writable:
		try:
			nextMsg = messageQueues[w].get_nowait()
		except Queue.Empty:
			print("output queue for ", w.getpeername(), " is empty")
			outputs.remove(w)
		else: 
			print("sending {} to {}".format(nextMsg, w.getpeername()))
			w.send(nextMsg)

	for e in exceptional:
		print("handling exceptional condition for {}".format(s.getpeername()))
		inputs.remove(e)

		if e in outputs:
			outputs.remove(e)
		e.close()

		del messageQueues[e]


