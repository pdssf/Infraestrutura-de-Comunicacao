#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer

# classe para gerenciar requisições HTTP
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET é sempre executado
  def do_GET(self):
        # Envia o status da resposta (200/OK)
        self.send_response(200)
 
        # parâmetros básicos do cabeçalho
        self.send_header('Content-type','text/html')
        self.end_headers()
        print(self.wfile)

        # menssagem que vai ser enviada para o cliente
        message = "sei la"
        # codifica a menssagem e envia
        self.wfile.write(bytes(message, "utf8"))
        #encerra a conexão
        self.close_connection = 1
        return
 
 # 'classe principal' que vai executar sempre
def run():
  print('Iniciando server...')
 
  #o servidor vai rodar localmente com a porta 8081 ativa
  server_address = ('localhost', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('Server online...')
  #método para não encerrar execução até que seja dado uma interrupção 
  httpd.serve_forever()
 
 
run()
