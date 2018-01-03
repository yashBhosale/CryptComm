import socket
import sys
import select

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server given by the caller
server_address = ('192.168.0.3', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address

try: 
  sock.connect(server_address)
except: 
  print 'Unable to connect'
  sys.exit()

print'Connected to remote host. You can start sending messages now.'

while 1:
  # writable and exceptional don't have any corresponding variables because
  # there's only one place to write to
  inputs = [sys.stdin, sock] 
  readable, writable, exceptional = select.select(inputs, [], [])

  for r in readable:

	if r == sys.stdin
		# user typed in a message
		msg = sys.stdin.readline()
		sock.send(msg)
	else if r == sock
		data = sock.recv(4096)
		if not data :
			# means the server disconnected
			print '\nDisconnected from chat server'
			sys.exit()
		else :
			#user entered a message
			sys.stdout.write(data)
			sys.stdout.write('You >')
			sys.stdout.flush()

  
