from socket import *

#criando objeto socket servidor com porta 12000
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print ('servidor criado!\n')

while 1:
	#aguarda requisição do cliente
    message, clientAddress = serverSocket.recvfrom(2048)

    #imprime mensagem decodificada
    print(message.decode('UTF-8','strict'))

    #capitaliza letras da menssagem
    modifiedMessage = message.upper()

    #envia mensagem capitalizada 
    serverSocket.sendto(modifiedMessage, clientAddress)
