from socket import *
from builtins import input

#Endereço e numero do socket que faremos comunicação (sevidor)
serverName = 'localhost'
serverPort = 12000

#Declarando o objeto socket cliente param.1 = IPV4;param.2 = sock UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)

#aplicação enviará essa menssagem
message = input('digite em letras minusculas:')

while(len(message)> 1):
    #função de passagem de menssagem deve ser codificada antes de mandar
    clientSocket.sendto(message.encode(),(serverName, serverPort))

    #aguarda resposta do servidor 
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    #Resposta do servidor a string deve ser decodificada antes de imprimir
    print (modifiedMessage.decode('UTF-8','strict'))
    message = input('Input lowercase sentence:')

#encerra o programa
clientSocket.close()
