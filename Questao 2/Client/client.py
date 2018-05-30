from socket import *
from builtins import input


#initial config
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
commandLine = ''

#asks for the user name
#initial exchange, login
userName = input( 'Please, type your username:' )
clientSocket.send(userName.encode())
while(commandLine != 'exit'):
    commandLine = input( 'Please, type your command: GET, PUT, clientSend or exit \n' )
    clientSocket.send(commandLine.encode())
    #sends command to the server and wait a response
    print('Waiting for command line')
    serverResponse = clientSocket.recv(1024)
    print('Resposta do servidor', serverResponse.decode())

    #sends file to server
    if(serverResponse.decode() == 'helo send me file'):
        #digita nome do arquivo
        fileName = input('Digite o nome do arquivo a ser enviado: \n')
        #envia nome do arquivo
        clientSocket.send(fileName.encode())
        sendingFile = open(fileName,'rb')
        sendingPart = sendingFile.read(1024)
        while (sendingPart):
            clientSocket.send(sendingPart)
            sendingPart = sendingFile.read(1024)
        sendingFile.close()
        print('sended file')
        #clientSocket.shutdown(clientSocket.SHUT_WR)

    #receives file from server
    elif(serverResponse.decode() == 'GET'):
        print('Client received GET back')
        fileName = input('What file would you like to download?\n')
        clientSocket.send(fileName.encode())#1
        receivingFile = open(fileName,'wb')
        #receivingPart = clientSocket.recv(1024)#2
        while(1):
            receivingPart = clientSocket.recv(1024)
            receivingFile.write(receivingPart)
            if len(receivingPart) < 1024:
                break
        receivingFile.close()
        print('received file')

    #to be implemented
    elif(serverResponse.decode() == 'PUT'):
        print('Client received PUT back')

    elif(commandLine == 'exit'):
        break

clientSocket.close()
