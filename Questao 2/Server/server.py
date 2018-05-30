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
	#login
	result = checkUserName(userName)
	while(commandLine != 'exit'):
		#menu
		print('Waiting for command line from client')
		commandLine = connectionSocket.recv(1024)
		print('Received. Client response: ',commandLine.decode())

		#possible user commands:
		#receives file from client
		if(commandLine.decode() == 'clientSend'):
			connectionSocket.send('helo send me file'.encode())
			#receives fileName
			fileName = connectionSocket.recv(1024)
			fileName = fileName.decode()
			print('received fileName:', fileName)
			#concatenate 'username' '/' 'fileName'
			path = userName.decode() + '/' + fileName
			receivingFile = open(path,'wb')
			#starts to receive the file
			receivingPart = connectionSocket.recv(1024)
			while(receivingPart):
				receivingFile.write(receivingPart)
				receivingPart = connectionSocket.recv(1024)
				if len(receivingPart) < 1024:
					break
			receivingFile.close()
			print('received file')

		#sends file to client
		elif(commandLine.decode() == 'GET'):
			connectionSocket.send(commandLine)
			print('waiting for file name')
			fileName = connectionSocket.recv(1024)#1
			fileName = fileName.decode()
			print('received file name')
			path = userName.decode() + '/' + fileName
			sendingFile = open(path,'rb')
			sendingPart = sendingFile.read(1024)
			while (sendingPart):
				connectionSocket.send(sendingPart)
				sendingPart = sendingFile.read(1024)
			sendingFile.close()
			print('sended file')


		#to be implemented
		elif(commandLine.decode() == 'PUT'):
			connectionSocket.send(commandLine)

		elif(commandLine.decode() == 'exit'):
			break
		else:
			connectionSocket.send(commandLine)
			print('wrong command line')
	connectionSocket.close()