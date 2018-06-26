import urllib.request
import urllib.parse

#cria-se uma variavel url com o endereço do hospedeiro http
url = 'http://localhost:8081'
#E então é feita uma requisiçao, as (in)convenienciencas são abstraidas no método
f = urllib.request.urlopen(url)
#É feito um print do conteudo recebido 
print(f.read().decode('utf-8'))
