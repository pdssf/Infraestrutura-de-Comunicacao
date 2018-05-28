from socket import *
from builtins import input

#Endereço e numero de socket do servidor
serverName = 'localhost'
serverPort = 12000

#Declarando o objeto socket cliente param.1 = IPV4;param.2 = sock TCP
clientSocket = socket(AF_INET, SOCK_STREAM)

#apresentação de 3 vias e criação da conecção TCP
clientSocket.connect((serverName,serverPort))

#mensagem a ser enviada
sentence = input( 'Input lowercase sentence:' )
#converte a string para binario e envia a mensagem ao server
clientSocket.send(sentence.encode())
#recebe a mensagem do server e volta de binario para string
modifiedSentence = clientSocket.recv(1024)
print ('From Server:', modifiedSentence.decode())
#encerra a conexão
clientSocket.close()
