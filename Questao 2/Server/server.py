#devido a como o manuseamento de arquivos é tratado neste programa
#o mesmo deve ser executado diretamente da pasta Server

from socket import *
import os
import pickle
import _thread

#Checa se o nome de usuário já está em uso, se nao estiver em uso
#uma nova pasta com esse nome sera criada
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

#adiciona ou remove uma entrada da database, baseando-se no comando
#do usuario
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

#funcao que representa o corpo do programa, será rodado para cada cliente
def connected (connectionSocket, addr):
	userName = connectionSocket.recv(1024)
	#recebe o login
	commandLine = ''
	result = checkUserName(userName)
	while(commandLine != 'exit'):
		#menu
		print('Waiting for command line from client')
		commandLine = connectionSocket.recv(1024)
		print('Received. Client response: ',commandLine.decode())

		#cada if está ligado a um possível comando dado pelo cliente
		#POST: recebe o nome do arquivo, abre o mesmo e escreve 
		#1024 bytes a cada loop. Quando recebe 'end', finaliza
		# 
		if(commandLine.decode() == 'POST'):
			connectionSocket.send('helo send me file'.encode())
			#recebe o nome do arquivo
			fileName = connectionSocket.recv(1024)
			fileName = fileName.decode()
			print('received fileName:', fileName)
			
			path = userName.decode() + '/' + fileName
			receivingFile = open(path,'wb')
			#começa a receber o arquivo
			#receivingPart = connectionSocket.recv(1024)
			while(1):
				receivingPart = connectionSocket.recv(1024)
				print('Recebeu Data', len(receivingPart))
				try:
					if(receivingPart.decode() == 'end'):
						break
				except:
					receivingFile.write(receivingPart)
					
				
			receivingFile.close()
			print('received file')
			databaseHandler(userName, 'POST', fileName)

		#GET: recebe o nome do arquivo e para cada loop
		#le 1024 bytes e os envia para o cliente
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
			connectionSocket.send('end'.encode())
			sendingFile.close()
			print('sended file')

		
		#ls: le o arquivo da database, o transformando em lista
		# e utilizando o pickle.dumps, transforma essa lista em uma
		# forma utilizavel pelo socket
		elif (commandLine.decode()=='ls'):
			#path = os.path.abspath(userName)
			connectionSocket.send(commandLine)
			sendingList = os.listdir(userName.decode())
			#sendingList = sendingList.encode()
			print(sendingList)
			sendingList = pickle.dumps(sendingList)
			connectionSocket.send(sendingList)
		
		#DELETE: recebe o nome de um arquivo e o deleta da pasta
		# e da database
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
#recebe uma conexao tcp e a atribui a uma thread, repete para cada nova conexao
while 1:
	connectionSocket, addr = serverSocket.accept()
	_thread.start_new_thread(connected, tuple([connectionSocket, addr]))	