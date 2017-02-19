import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server given by the caller
server_address = ('192.168.0.3', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
   closeConnection = ('seshclose')
   message = ''
   while message is not closeConnection:
    message = raw_input()

    if message == 'seshclose':
    	sock.shutdown(1)
        break
    
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)

    

finally:
    sock.close()



