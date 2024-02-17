import lexer
import parser_1 
with open('pruebas.txt', 'r') as archivo:
    contenido = archivo.read()

lista = [] 
contenido = contenido.split('\n') 
for linea in contenido: 
    result = lexer.run(linea) 
    lista.append(result)

parser =parser_1.parser(lista) 
print(parser)
   