from socket import *

#criando objeto socket servidor com porta 12000
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print ('servidor criado!\n')

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(message.decode('UTF-8','strict'))
    modifiedMessage = message.upper()
    serverSocket.sendto(modifiedMessage, clientAddress)
