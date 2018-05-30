from socket import *
import os

#checks if username is already in use, if not will create
#a new folder for the user
def checkUserName( userName ):
    if not os.path.exists(userName):
        print('New user, creating new directory..\n')
        os.makedirs(userName)
        return 'new'
    else:
        print('Old user: ', userName.decode())
        return 'old'
    return

#initial config
commandLine = ''
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
while 1:
	connectionSocket, addr = serverSocket.accept()
	userName = connectionSocket.recv(1024)
	result = checkUserName(userName)
	while(commandLine != 'exit'):
		print('Waiting for command line from client')
		commandLine = connectionSocket.recv(1024)
		print('Received. Client response: ',commandLine.decode())

		#possible user commands
		if(commandLine.decode() == 'GET'):
			connectionSocket.send(commandLine)
		elif(commandLine.decode() == 'PUT'):
			connectionSocket.send(commandLine)
		elif(commandLine.decode() == 'exit'):
			break
		else:
			connectionSocket.send(commandLine)
			print('wrong command line')
	connectionSocket.close()