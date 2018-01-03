#completely untested as of 2:11 AM 1/2/18 

import socket
import sys
import select
import sqlite3
import Queues

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# dataBase = sqlite3.connect('users.db')
# db = dataBase.cursor()

# There's going to be some TLS here, but cross that bridge once you get to it, I suppose.

# Bind socket to self
server_address = ('localhost', 80)

print >>sys.stderr, 'starting up on %s port %s' % server_address 

sock.bind(server_address)
sock.listen(5)

###############################################################


inputs = [ sock ]
messageQueues = {}

while inputs:
readable, writable, error = select(inputs, outputs, inputs)

	for s in readable:
		if s is sock 
			#this means there's a new connection

			connection, client_address = sock.accept()
			connection.setblocking(0)
			
			# if usercheck(db, connection) is True:
			inputs.append(connection)
			messageQueues[connection] = Queues.queue()
		

		else:
			data = connection.recv(64)
			if data:
				# accept their data, put them in the output list if
				# they're not already there, and put that message 
				# in every client's message queue
				
				if s not in outputs
					outputs.append(s)
				for client in messageQueues
					messageQueues[client].put(data)
			else:
				# a readable socket with no data is an empty connection.
				# remove them both from outputs and inputs
				
				if s in outputs
					outputs.remove(s)
				inputs.remove(s)
				s.close()

	for w in writable:
		try:
			nextMsg = messageQueues[w].get_nowait()
		except Queue.Empty:
			print >>sys.stderr 'output queue for', w.getpeername(), 'is empty'
			outputs.remove(w)
		else: 
			print >>sys.stderr 'sending %s to %s' % (nextMsg, w.getpeername())
			w.send(nextMsg)

	for e in exceptional:
		print >>sts.stderr, 'handling exceptional condition for', s.getpeername()
		inputs.remove(e)

		if e in outputs:
			outputs.remove(e)
		e.close()

		del messageQueues[e]

#def usercheck(db, connection):

#	#SANITIZE THESE
#	connection.send('Please input a username')
#	user = connection.recv(64)

#	connection.send('Please input  password')
#	password = connection.recv(64)
#	sanitized = (password,)

	#hashing stuff
#	db.execute("SELECT password FROM users WHERE username=?", sanitized)
#	check = db.fetchone()

#	if password == check:
#		return True
#	else:
#		return False

