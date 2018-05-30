from socket import *
from builtins import input


#initial config
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
commandLine = ''

#asks for the user name
#initial exchange
userName = input( 'Please, type your username:' )
clientSocket.send(userName.encode())
while(commandLine != 'exit'):
    commandLine = input( 'Please, type your command: GET, PUT or exit \n' )
    clientSocket.send(commandLine.encode())
    print('Waiting for command line')
    serverResponse = clientSocket.recv(1024)
    print('Resposta do servidor', serverResponse.decode())
    if(serverResponse.decode() == 'GET'):
        print('Client received GET back')
    elif(serverResponse.decode() == 'PUT'):
        print('Client received PUT back')
    elif(commandLine == 'exit'):
        break

clientSocket.close()
