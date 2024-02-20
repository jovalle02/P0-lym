import lexer

file_path = 'pruebas.txt'  # Replace with the actual path to your file

with open(file_path, 'r') as file:
    lines = file.readlines()

text = ''.join(lines).replace('\n', '')

result, error = lexer.run('<stdin>', text)

if error:
    print(error.as_string())
elif result:
    print(repr(result))