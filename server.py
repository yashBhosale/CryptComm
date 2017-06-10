#completely untested as of 2:11 AM 6/11/17 

import socket
import sys
import select
import sqlite3
import Queues

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dataBase = sqlite3.connect('users.db')
db = dataBase.cursor()

# Bind socket to self
server_address = (sock.gethostname(), 80)

print >>sys.stderr, 'starting up on %s port %s' % server_address 

sock.bind(server_address)
sock.listen(5)


#we need to check for stuff like 

###############################################################


inputs = [ sock ]
messageQueues = {}

while inputs:
readable, writable, error = select(inputs, outputs, inputs)

	for s in readable:
		if s is server #this means there's a new connection

			connection, client_address = sock.accept()
			#I think this is where initial authentication goes

			connection.setblocking(0)
			
			if usercheck(db, connection) is True:
				inputs.append(connection)
				messageQueues[connection] = Queues.queue()
		

		else:
			data = connection.recv(64)
			if data:
				if s not in outputs
					outputs.append(s)
				for clients in messageQueues
					messageQueues[client].put(data)
			else:
				if s in outputs
					outputs.remove(s)
					inputs.remove(s)
					s.close()

	for w in writable:
		try:
			nextMsg = messageQueues[w].get_nowait()
		except: Queue.Empty:
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
		s.close()

		del messageQueues[e]

def usercheck(db, connection):

	#SANITIZE THESE
	connection.send('Please input a username')
	user = connection.recv(64)

	connection.send('Please input  password')
	password = connection.recv(64)
	sanitized = (password,)

	#hashing stuff
	db.execute("SELECT password FROM users WHERE username=?", sanitized)
	check = db.fetchone()

	if password == check:
		return True
	else:
		return False

