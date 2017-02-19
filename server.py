import socket
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random


key = b'very large generated key'

iv = Random.new().read(AES.block_size)

newCipher = AES.new(key,AES.MODE_CFB, iv)

chatLog = open('chatlog.txt', 'w')

chatLog.close()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



server_address = ('192.168.0.2', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)

while True:
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()
	chatLog = open('chatlog.txt', 'a')
	try:
		print >>sys.stderr, 'client connected:', client_address
		while True:
			data = connection.recv(64)
			
			print >>sys.stderr, 'received "%s"' % data
			if data:
				connection.sendall(data)
				encryptedMessage = iv + newCipher.encrypt(data)
				chatLog.write(encryptedMessage + '\n')
			else:
				break
	finally:
		connection.close()

	chatLog.close()