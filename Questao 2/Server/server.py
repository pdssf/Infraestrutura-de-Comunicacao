#to avoid problems, go to the server folder and then run this file

from socket import *
import os
import pickle #to send and receive lists
import _thread

#checks if username is already in use, if not will create
#a new folder for the user
def checkUserName( userName ):
	if not os.path.exists(userName):
		print('New user, creating new directory..\n')
		os.makedirs(userName)
		databasePath = userName.decode() + '.txt'
		database = open(databasePath, 'x')
		database.close()
		return 'new'
	else:
		print('Old user: ', userName.decode())
		return 'old'

#adds or removes the file from the database
def databaseHandler(userName, mode, fileName):
	databasePath = userName.decode() + '.txt'
	database = open(databasePath, 'a+')
	database.close()
	database = open(databasePath, 'r')
	lines = database.readlines()
	database.close()
	if(mode == 'POST'):
		#write in file
		notFind = 1
		print(lines)
		for line in lines:
			#print('1')
			#print('linha:',line)
			if line == fileName + '\n':
				#print('Achou!')
				notFind = 0
		if notFind:
			print('notfind')
			database = open(databasePath, 'a')
			database.write(fileName + '\n')
			database.close()
	elif(mode == 'DELETE'):
		database = open(databasePath,'w')
		print(lines)
		for line in lines:
			print(line)
			if (line != (fileName.decode()+'\n')):
				database.write(line)
		database.close()

#runs for each client, one per thread
def connected (connectionSocket, addr):
	userName = connectionSocket.recv(1024)
	#login
	commandLine = ''
	result = checkUserName(userName)
	while(commandLine != 'exit'):
		#menu
		print('Waiting for command line from client')
		commandLine = connectionSocket.recv(1024)
		print('Received. Client response: ',commandLine.decode())

		#possible user commands:
		#receives file from client
		if(commandLine.decode() == 'POST'):
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
				if(receivingPart != 'end'.encode()):
					receivingPart = connectionSocket.recv(1024)
				if len(receivingPart) < 1024:
					break
			receivingFile.close()
			print('received file')
			databaseHandler(userName, 'POST', fileName)

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

		
		#ls
		elif (commandLine.decode()=='ls'):
			#path = os.path.abspath(userName)
			connectionSocket.send(commandLine)
			sendingList = os.listdir(userName.decode())
			#sendingList = sendingList.encode()
			print(sendingList)
			sendingList = pickle.dumps(sendingList)
			connectionSocket.send(sendingList)
		
		elif (commandLine.decode() == 'DELETE'):
			connectionSocket.send(commandLine)
			print('Waiting for fileName')
			fileName = connectionSocket.recv(1024)
			path = userName.decode() + '/' + fileName.decode()
			if os.path.exists(path):
				os.remove(path)
			databaseHandler(userName, 'DELETE', fileName)

		elif(commandLine.decode() == 'exit'):
			break

		else:
			connectionSocket.send(commandLine)
			print('wrong command line')
	connectionSocket.close()
	
#initial config
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
#tudo igual
while 1:
	connectionSocket, addr = serverSocket.accept()
	_thread.start_new_thread(connected, tuple([connectionSocket, addr]))
	#igual
	