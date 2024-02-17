def parser(tokens):
    program = {}
    with open('program.txt', 'r') as archivo:
    #contenido = archivo.read() 
        for linea in archivo : 
            linea = linea.split('->') 
            program[linea[0]] = linea[1].replace('\n', '').split(',') 
    #tokens = tokens[0]
    tokensCorrectos = []
    for line in tokens: 
        
        firstToken = line[0]
        firstToken = str(firstToken)
        firstToken = firstToken[:firstToken.index(':')] 
        estructura = program[firstToken] 
        estructura = program[estructura[0]][0]
        estructura = estructura.split(' ') 
        for i in range(0, len(estructura)): 
            edidarlinea = line[i]
            edidarlinea= str(edidarlinea)
            edidarlinea= edidarlinea[:edidarlinea.index(':')]
            if estructura[i] == edidarlinea: 
                tokensCorrectos.append(True)
            else:
                tokensCorrectos.append(False)
    return True if False not in tokensCorrectos else False 
    
            
           
            