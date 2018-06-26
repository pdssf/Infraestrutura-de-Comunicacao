#devido a como o manuseamento de arquivos é tratado neste programa
#o mesmo deve ser executado diretamente da pasta Client

from socket import *
from builtins import input
import pickle


#configuracoes iniciais
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
commandLine = ''

#pede ao cliente o nome de usuário e o envia ao servidor
userName = input( 'Please, type your username:' )
clientSocket.send(userName.encode())
while(commandLine != 'exit'):
    #pede o comando ao usuário e em seguida o envia ao servidor
    commandLine = input( 'Please, type your command: GET, POST, ls, DELETE or exit \n' )
    clientSocket.send(commandLine.encode())
    print('Waiting for command line')
    serverResponse = clientSocket.recv(1024)
    #recebe resposta do servidor para seguir com o procedimento devido
    #de cada comando
    print('Resposta do servidor', serverResponse.decode())

    #POST: envia arquivo ao servidor, lendo 1024 bytes e os enviando
    #a cada loop, envia 'end' para sinalizar o fim
    if(serverResponse.decode() == 'helo send me file'):
        #digita nome do arquivo
        fileName = input('Type the name of the file to be sended: \n')
        #envia nome do arquivo
        clientSocket.send(fileName.encode())
        sendingFile = open(fileName,'rb')
        sendingPart = sendingFile.read(1024)
        while (sendingPart):
            clientSocket.send(sendingPart)
            print('Sending Data')
            sendingPart = sendingFile.read(1024)
        sendingFile.close()
        clientSocket.send('end'.encode())
        #clientSocket.send('end'.encode())
        print('sended file')
        #clientSocket.shutdown(clientSocket.SHUT_WR)

    #GET: envia um nome de um arquivo para o servidor
    #cria um novo arquivo e escreve de 1024 em 1024 bytes
    #nesse novo arquivo, replicando o arquivo do servidor
    elif(serverResponse.decode() == 'GET'):
        print('Client received GET back')
        fileName = input('What file would you like to download?\n')
        clientSocket.send(fileName.encode())#1
        receivingFile = open(fileName,'wb')
        #receivingPart = clientSocket.recv(1024)#2
        while(1):
            receivingPart = clientSocket.recv(1024)
            try:
                if(receivingPart.decode()=='end'):
                    break
            except:
                receivingFile.write(receivingPart)
            
        receivingFile.close()
        print('received file')


    #ls: recebe uma lista codificada do servidor
    # , a decodifica usando o pickle.loads
    #e a imprime para o usuário
    elif(serverResponse.decode() == 'ls'):
        receivingList = clientSocket.recv(1024)
        receivingList = pickle.loads(receivingList)
        print(receivingList)

    #DELETE: recebe uma entrada de nome de arquivo do usuário
    #e o envia para o servidor (que por sua vez irá deletar o arquivo
    # que possui este nome)
    elif (serverResponse.decode() == 'DELETE'):
        fileName = input('What file would you like to delete?\n')
        clientSocket.send(fileName.encode())
        pass

    elif(commandLine == 'exit'):
        break

clientSocket.close()
