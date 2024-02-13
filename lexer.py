import string


LETTERS = string.ascii_letters
DIGITS = '0123456789'


#System-specific keywords

FUNCTION_KEYWORDS = {
    'defvar': 'DEFVARKEYWORD',
    'move': 'MOVEFUNCTION',
    'skip': 'SKIPFUNCTION',
    'turn': 'TURNFUNCTION',
    'face': 'FACEFUNCTION',
    'put': 'PUTFUNCTION',
    'pick': 'PICKFUNCTION',
    'move-dir': 'MOVEDIRFUNCTION',
    'run-dirs': 'RUNDIRSFUNCTION',
    'move-face': 'MOVEFACEFUNCTION',
    'null': 'NULL',
}

#Constant-specific keywords
KEYWORD_CONSANTS = {
    'Dim': 'DIMENSIONBOARDCONSTANT',
    'myXpos': 'POSITIONXCONSTANT',
    'myYpos': 'POSITIONYCONSTANT',
    'myChips': 'CHIPSCONSTAT',
    'myBallons': 'SELFBALLONSCONSTANT',
    'ballonsHere': 'CELLBALLONSCONSTANT',
    'ChipsHere': 'AVAILABLECHIPSCONSTANT',
    'Spaces': 'POSSIBLECHIPSDROPCONSTANT',
    ':left': 'LEFTCONSTANT',
    ':right': 'RIGHTCONSTANT',
    ':around': 'AROUNDCONSTANT',
    ':north': 'NORTHCONSTANT',
    ':south': 'SOUTHCONSTANT',
    ':east': 'EASTCONSTANT',
    ':west': 'WESTCONSTANT',
    ':balloons': 'BALLONSCONSTANT',
    ':chips': 'CHIPSCONSTANT',
    ':front': 'FRONTCONSTANT',
    ':back': 'BACKCONSTANT',
}

#Control_Structure-specific keywords
CONTROL_STRUCTURE_KEYWORDS = {
    'if': 'IF',
    'loop': 'LOOP',
    'repeat': 'REPEAT'
}

#Condition-specific keywords
CONDITIONAL_KEYWORDS = {
    'facing?': 'FACINGCONDITION',
    'blocked?': 'BLOCKEDCONDITION',
    'can-put?': 'CANPUTCONDITION',
    'can-pick?': 'CANPICKCONDITION',
    'can-move?': 'CANMOVECONDITION',
    'isZero?': 'ISZEROCONDITION',
    'not': 'NEGCONDITION',
}



class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
        
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        
    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self.current_char in ' ':
                self.advance()
            elif self.current_char == "=":
                tokens.append(Token('TARGETVARIABLE', self.current_char))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token("OPENPARENTHESIS", self.current_char))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token("CLOSINGPARENTHESIS", self.current_char))
                self.advance()
            elif self.current_char == ':':
                tokens.append(self.make_constant())
            elif self.current_char in (LETTERS + '-' + '?' + DIGITS):
                tokens.append(self.make_identifiers())

                
        return tokens
                
    def make_identifiers(self):
        id_str = ''
        
        while self.current_char != None and self.current_char in LETTERS + '-' + '?' + DIGITS:
            id_str += self.current_char
            self.advance()
            
        if id_str in CONDITIONAL_KEYWORDS.keys():
            return Token(CONDITIONAL_KEYWORDS[id_str], id_str)
        elif id_str in CONTROL_STRUCTURE_KEYWORDS.keys():
            return Token(CONTROL_STRUCTURE_KEYWORDS[id_str], id_str)
        elif id_str in KEYWORD_CONSANTS.keys():
            return Token(KEYWORD_CONSANTS[id_str], id_str)
        elif id_str in  FUNCTION_KEYWORDS.keys():
            return Token(FUNCTION_KEYWORDS[id_str], id_str)
        elif id_str.isdigit():
            return Token('VALUE', id_str)
        else:
            return Token('VARIABLE', id_str)
        
    def make_constant(self):
        id_str = ''
        
        while self.current_char != None and self.current_char in (LETTERS + '-' + '?' + DIGITS +':'):
            id_str += self.current_char
            self.advance()
            
        if id_str in KEYWORD_CONSANTS.keys():
            return Token(KEYWORD_CONSANTS[id_str], id_str)
        else:
            return Token('UNKNOWNCONSTANT', id_str)
    
    
def run(text):
    lexer = Lexer(text)
    tokens = lexer.make_tokens()
        
    return tokens