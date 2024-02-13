import lexer

while True:
    text = input(">")
    result = lexer.run(text)
    
    print(result)