import string
from str_arrows import *


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

VALUE_CONSTANTS = {
    'Dim': 'DIMENSIONBOARDCONSTANT',
    'myXpos': 'POSITIONXCONSTANT',
    'myYpos': 'POSITIONYCONSTANT',
    'myChips': 'CHIPSCONSTAT',
    'myBallons': 'SELFBALLONSCONSTANT',
    'ballonsHere': 'CELLBALLONSCONSTANT',
    'ChipsHere': 'AVAILABLECHIPSCONSTANT',
    'Spaces': 'POSSIBLECHIPSDROPCONSTANT', 
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

class Position:
  def __init__(self, index, line, col, fn, ftxt):
    self.index = index
    self.line = line
    self.col = col
    self.fn = fn
    self.ftxt = ftxt

  def advance(self, current_char=None):
    self.index += 1
    self.col += 1

    if current_char == '\n':
      self.line += 1
      self.col = 0

    return self

  def copy(self):
    return Position(self.index, self.line, self.col, self.fn, self.ftxt)


class Token:
    def __init__(self, type_, value=None, pos_start = None, pos_end=None):
        self.type = type_
        self.value = value
        
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()
        
    def matches(self, type_):
        return self.type == type_
        
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    
class Lexer:
    
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
        
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None
        
    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self.current_char in ' ':
                self.advance()
            elif self.current_char == "=":
                tokens.append(Token('TARGETVARIABLE', self.current_char, pos_start=self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token("OPENPARENTHESIS", self.current_char, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token("CLOSINGPARENTHESIS", self.current_char, pos_start=self.pos))
                self.advance()
            elif self.current_char == ':':
                tokens.append(self.make_constant())
            elif self.current_char in (LETTERS + '-' + '?' + DIGITS):
                tokens.append(self.make_identifiers())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
                

        tokens.append(Token('EOF', pos_start=self.pos))        
        return tokens
                
    def make_identifiers(self):
        pos_start = self.pos.copy()
        id_str = ''
        
        while self.current_char != None and self.current_char in LETTERS + '-' + '?' + DIGITS:
            id_str += self.current_char
            self.advance()
            
        if id_str in CONDITIONAL_KEYWORDS.keys():
            return Token(CONDITIONAL_KEYWORDS[id_str], id_str, pos_start, self.pos)
        elif id_str in CONTROL_STRUCTURE_KEYWORDS.keys():
            return Token(CONTROL_STRUCTURE_KEYWORDS[id_str], id_str, pos_start, self.pos)
        elif id_str in KEYWORD_CONSANTS.keys():
            return Token(KEYWORD_CONSANTS[id_str], id_str, pos_start, self.pos)
        elif id_str in  FUNCTION_KEYWORDS.keys():
            return Token(FUNCTION_KEYWORDS[id_str], id_str, pos_start, self.pos)
        elif id_str.isdigit():
            return Token('VALUE', id_str, pos_start, self.pos)
        else:
            return Token('VARIABLE', id_str, pos_start, self.pos)
        
    def make_constant(self):
        pos_start = self.pos.copy()
        id_str = ''
        
        while self.current_char != None and self.current_char in (LETTERS + '-' + '?' + DIGITS +':'):
            id_str += self.current_char
            self.advance()
            
        if id_str in KEYWORD_CONSANTS.keys():
            return Token(KEYWORD_CONSANTS[id_str], id_str, pos_start, self.pos)
        else:
            return Token('UNKNOWNCONSTANT', id_str, pos_start, self.pos)
        
class Error:
  def __init__(self, pos_start, pos_end, error_name, details):
    self.pos_start = pos_start
    self.pos_end = pos_end
    self.error_name = error_name
    self.details = details
  
  def as_string(self):
    result  = f'{self.error_name}: {self.details}\n'
    result += f'File {self.pos_start.fn}, line {self.pos_start.line + 1}'
    result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
    return result

class IllegalCharError(Error):
  def __init__(self, pos_start, pos_end, details):
    super().__init__(pos_start, pos_end, 'Illegal Character', details)

class ExpectedCharError(Error):
  def __init__(self, pos_start, pos_end, details):
    super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
  def __init__(self, pos_start, pos_end, details=''):
    super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RTError(Error):
  def __init__(self, pos_start, pos_end, details, context):
    super().__init__(pos_start, pos_end, 'Runtime Error', details)
    self.context = context

  def as_string(self):
    result  = self.generate_traceback()
    result += f'{self.error_name}: {self.details}'
    result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
    return result

  def generate_traceback(self):
    result = ''
    pos = self.pos_start
    ctx = self.context

    while ctx:
      result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
      pos = ctx.parent_entry_pos
      ctx = ctx.parent

    return 'Traceback (most recent call last):\n' + result

##########################33

#NODES
    
class defvarNode:
    def __init__(self, variable_name_node, value_node):
        self.variable_node_name = variable_name_node
        self.value_node = value_node
        
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end
        
    def __repr__(self):
        return f'({self.variable_node_name}, {self.value_node})'
            
class defunNode:
    def __init__(self, left_node, params_node, body_node):
        self.left_node = left_node
        self.body_node = body_node
        self.params_node = params_node
        
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end
        
    def __repr__(self):
        return f'({self.left_node}, {self.body_node}, {self.params_node})'
    
class moveNode:
    def __init__(self, value_node):
        self.value_node = value_node
        
        self.pos_start = self.value_node.pos_start
        self.pos_end = self.value_node.pos_end
    def __repr__(self):
        return f'{self.value_node}'
    
class skipNode:
    def __init__(self, value_node):
        self.value_node = value_node
        
        self.pos_start = self.value_node.pos_start
        self.pos_end = self.value_node.pos_end
    def __repr__(self):
        return f'{self.value_node}'
    
class faceNode:
    def __init__(self, value_node):
        self.value_node = value_node
        
        self.pos_start = self.value_node.pos_start
        self.pos_end = self.value_node.pos_end
    def __repr__(self):
        return f'{self.value_node}'
    
class turnNode:
    def __init__(self, value_node):
        self.value_node = value_node
        
        self.pos_start = self.value_node.pos_start
        self.pos_end = self.value_node.pos_end
    def __repr__(self):
        return f'{self.value_node}'
    
class putNode:
    def __init__(self, var_name_node, value_node):
        self.var_name_node = var_name_node
        self.value_node = value_node
        
        self.pos_start = self.var_name_node.pos_start
        self.pos_end = self.value_node.pos_end
        
class pickNode:
    def __init__(self, var_name_node, value_node):
        self.var_name_node = var_name_node
        self.value_node = value_node
        
        self.pos_start = self.var_name_node.pos_start
        self.pos_end = self.value_node.pos_end
        
class moveDirsNode:
    def __init__(self, var_name_node, value_node):
        self.var_name_node = var_name_node
        self.value_node = value_node
        
        self.pos_start = self.var_name_node.pos_start
        self.pos_end = self.value_node.pos_end
        
class runDirsNode:
    def __init__(self, value_node):
        self.value_node = value_node
        
        self.pos_start = self.var_name_node.pos_start
        self.pos_end = self.value_node.pos_end
        
class moveFaceNode:
    def __init__(self, var_name_node, value_node):
        self.var_name_node = var_name_node
        self.value_node = value_node
        
        self.pos_start = self.var_name_node.pos_start
        self.pos_end = self.value_node.pos_end
           
class IfNode:
    def __init__(self, condition_node, body_node, else_body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        self.else_body_node = else_body_node
        
        # Assuming condition_node, body_node, and else_body_node have pos_start and pos_end attributes
        self.pos_start = condition_node.pos_start
        self.pos_end = else_body_node.pos_end
    
class loopNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        
        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end
        
    def __repr__(self):
        return f'{self.condition_node}, {self.body_node}'
    
class repetTimesNode:
    def __init__(self, value_node, body_node):
        self.value_node = value_node
        self.body_node = body_node
        
        self.pos_start = self.value_node.pos_start
        self.pos_end = self.body_node.pos_end
    def __repr__(self):
        return f'{self.value_node}, {self.body_node}'
    
class targetVariableNode:
    def __init__(self, variable_name_node, value_node):
        self.variable_name_node = variable_name_node
        self.value_node = value_node
        
        self.pos_start = self.variable_name_node.pos_start
        self.pos_end = self.value_node.pos_end
    def __repr__(self):
        return f'{self.variable_name_node}, {self.value_node}'
    
class varAssignNode:
    def __init__(self, var_name_node, value_node):
        self.var_name_node = var_name_node
        self.value_node = value_node
        
        self.pos_start = self.var_name_node.pos_start
        self.pos_end = self.value_node.pos_end
        
class valueNode:
    def __init__(self, value_node):
        self.value_node = value_node
        
        self.pos_start = self.value_node.pos_start
        self.pos_end = self.value_node.pos_end
    def __repr__(self):
        return f'{self.value_node}'
    
class notConditional:
    def __init__(self, value_node):
        self.value_node = value_node
        
        self.pos_start = self.value_node.pos_start
        self.pos_end = self.value_node.pos_end
    def __repr__(self):
        return f'{self.value_node}'
    
class conditional:
    def __init__(self, value_node):
        self.value_node = value_node
        
        self.pos_start = self.value_node.pos_start
        self.pos_end = self.value_node.pos_end
    def __repr__(self):
        return f'{self.value_node}'
    
class nullNode:
    def __init__(self, value_node):
        self.value_node = value_node
        
        self.pos_start = self.value_node.pos_start
        self.pos_end = self.value_node.pos_end
    def __repr__(self):
        return f'{self.value_node}'

class constantNode:
    def __init__(self, name_node):
        self.name_node = name_node
        
        self.pos_start = self.name_node.pos_start
        self.pos_end = self.name_node.pos_end
    def __repr__(self):
        return f'{self.name_node}'
    
####### ESTABLISH GLOBAL VARIABLES ######
globalVariables = {}
    
#PERSERASULT
    
class ParseResult:
  def __init__(self):
    self.error = None
    self.node = None
    self.last_registered_advance_count = 0
    self.advance_count = 0

  def register_advancement(self):
    self.last_registered_advance_count = 1
    self.advance_count += 1

  def register(self, res):
    self.last_registered_advance_count = res.advance_count
    self.advance_count += res.advance_count
    if res.error: self.error = res.error
    return res.node

  def success(self, node):
    self.node = node
    return self

  def failure(self, error):
    if not self.error or self.last_registered_advance_count == 0:
      self.error = error
    return self
    
#PARSER

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()
        
    def advance(self, ):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token
    
    def parse(self):
        res = self.expr()
        if not res.error and self.current_token.type != 'EOF':
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected"
            ))
        return res
    
    def expr(self):
        res = ParseResult()
        
        if self.current_token.matches('OPENPARENTHESIS'):
            res.register_advancement()
            self.advance()
            if self.current_token.matches('DEFVARKEYWORD'):
                res.register_advancement()
                self.advance()
                
                if self.current_token.type != 'VARIABLE':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected variable name"))
                
                var_name = self.current_token
                res.register_advancement()
                self.advance()
                
                if self.current_token.type != 'VALUE':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected variable value"))
                    
                value = self.current_token
                res.register_advancement()
                self.advance()
                                
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis"))
                    
                res.register_advancement()
                self.advance()
                globalVariables[var_name.value] = value.value
                
                return res.success(varAssignNode(var_name, value))
            elif self.current_token.matches('TARGETVARIABLE'):
                res.register_advancement()
                self.advance()
                
                if self.current_token.value not in globalVariables.keys():
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Variable not existant"))
                    
                variable = self.current_token
                res.register_advancement()
                self.advance()
                
                if not (self.current_token.value not in globalVariables.keys()) or self.current_token.type != 'VALUE' or not(self.current_token.type not in VALUE_CONSTANTS.values()):
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected value for the variable"))
                    
                value = self.current_token
                res.register_advancement()
                self.advance()
                
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis"))  
                    
                res.register_advancement()
                self.advance()
                globalVariables[variable.value] = value.value
                
                return res.success(targetVariableNode(variable, value))
        
            elif self.current_token.matches('MOVEFUNCTION'):
                res.register_advancement()
                self.advance()
                
                first = False
                second = False
                third = False
                
                if self.current_token.value not in globalVariables.keys():
                    first = True
                    
                if self.current_token.type not in VALUE_CONSTANTS.values():
                    second = True
                    
                if self.current_token.type != 'VALUE':
                    third = True
                    
                if first and second and third:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected either a variable, constant or value."))
                        
                value = self.current_token  
                res.register_advancement()
                self.advance()
                    
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                                self.current_token.pos_start, self.current_token.pos_end,
                                "Expected closing parenthesis"))  
                    
                res.register_advancement()
                self.advance()
                return res.success(moveNode(value))
            elif self.current_token.matches('SKIPFUNCTION'):
                res.register_advancement()
                self.advance()
                
                first = False
                second = False
                third = False
                
                if self.current_token.value not in globalVariables.keys():
                    first = True
                    
                if self.current_token.type not in VALUE_CONSTANTS.values():
                    second = True
                    
                if self.current_token.type != 'VALUE':
                    third = True
                    
                if first and second and third:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected either a variable, constant or value."))
                    
                value = self.current_token  
                res.register_advancement()
                self.advance()
                
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis"))  
                
                res.register_advancement()
                self.advance()
                
                return res.success(skipNode(value))
            
            elif self.current_token.matches('TURNFUNCTION'):
                res.register_advancement()
                self.advance()
                
                if self.current_token.type not in [':around', ':left', ':right']:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected :around, :left or :right constants"))
                    
                value = self.current_token  
                res.register_advancement()
                self.advance()
                
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis"))  
                
                res.register_advancement()
                self.advance()
                
                return res.success(turnNode(value))

            elif self.current_token.matches('FACEFUNCTION'):
                res.register_advancement()
                self.advance()
                
                if self.current_token.value not in [":north", ":south", ":east", ":west"]:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected ':north', ':south', ':east' or ':west' constants"))
                    
                value = self.current_token  
                res.register_advancement()
                self.advance()
                
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis"))  
                
                res.register_advancement()
                self.advance()
                
                return res.success(faceNode(value))
            
            elif self.current_token.matches('PUTFUNCTION'):
                res.register_advancement()
                self.advance()
                
                if self.current_token.value not in [":balloons", ":chips"]:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected ':balloons' or ':chips' constants"))
                    
                typeof = self.current_token  
                res.register_advancement()
                self.advance()
                
                first = False
                second = False
                third = False
                
                if self.current_token.value not in globalVariables.keys():
                    first = True
                    
                if self.current_token.type not in VALUE_CONSTANTS.values():
                    second = True
                    
                if self.current_token.type != 'VALUE':
                    third = True
                    
                if first and second and third:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected either a variable, constant or value."))
                    
                value = self.current_token  
                res.register_advancement()
                self.advance()
                
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis"))  
                
                res.register_advancement()
                self.advance()
                
                return res.success(putNode(typeof, value))
            
            elif self.current_token.matches('PICKFUNCTION'):
                res.register_advancement()
                self.advance()
                
                if self.current_token.value not in [":balloons", ":chips"]:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected ':balloons' or ':chips' constants"))
                    
                typeof = self.current_token  
                res.register_advancement()
                self.advance()
                
                first = False
                second = False
                third = False
                
                if self.current_token.value not in globalVariables.keys():
                    first = True
                    
                if self.current_token.type not in VALUE_CONSTANTS.values():
                    second = True
                    
                if self.current_token.type != 'VALUE':
                    third = True
                    
                if first and second and third:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected either a variable, constant or value."))
                    
                value = self.current_token  
                res.register_advancement()
                self.advance()
                
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis"))  
                
                res.register_advancement()
                self.advance()
                
                return res.success(pickNode(typeof, value))

            elif self.current_token.matches('MOVEDIRFUNCTION'):
                res.register_advancement()
                self.advance()
                
                first = False
                second = False
                third = False
                
                if self.current_token.value not in globalVariables.keys():
                    first = True
                    
                if self.current_token.type not in VALUE_CONSTANTS.values():
                    second = True
                    
                if self.current_token.type != 'VALUE':
                    third = True
                    
                if first and second and third:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected either a variable, constant or value."))

                value = self.current_token  
                res.register_advancement()
                self.advance()
                
                if self.current_token.value not in [":front", ":right", ":left", ":back"]:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            'Expected ":front", ":right", ":left" or ":back" constants'))
                    
                typeof = self.current_token  
                res.register_advancement()
                self.advance()
                
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis"))  
                
                res.register_advancement()
                self.advance()
                
                return res.success(moveDirsNode(typeof, value))
            
            elif self.current_token.matches('RUNDIRSFUNCTION'):
                res.register_advancement()
                self.advance()
                
                statements = []
                
                while self.current_token.type != 'CLOSINGPARENTHESIS' or self.current_token.type not in [":front", ":right", ":left", ":back"]:
                    if self.current_token.type not in [":front", ":right", ":left", ":back"]:
                        return res.failure(InvalidSyntaxError(
                                self.current_token.pos_start, self.current_token.pos_end,
                                'Expected ":front", ":right", ":left" or ":back" constants'))
                    statements.append(self.current_token)
                    self.advance()
                    
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis"))
                else:
                    res.register_advancement()
                    self.advance()
                    return res.success(runDirsNode(statements))

            elif self.current_token.matches('NULL'):
                
                value = self.current_token
                res.register_advancement()
                self.advance()
                
                
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis"))
                    
                res.register_advancement()
                self.advance()
                
                return res.success(nullNode(value))
            
            elif self.current_token.matches('MOVEFACEFUNCTION'):
                res.register_advancement()
                self.advance()
                
                first = False
                second = False
                third = False
                
                if self.current_token.value not in globalVariables.keys():
                    first = True
                    
                if self.current_token.type not in VALUE_CONSTANTS.values():
                    second = True
                    
                if self.current_token.type != 'VALUE':
                    third = True
                    
                if first and second and third:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected either a variable, constant or value."))

                value = self.current_token  
                res.register_advancement()
                self.advance()
                
                if self.current_token.value not in [":north", ":south", ":east", ":west"]:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            'Expected ":front", ":right", ":left" or ":back" constants'))
                    
                typeof = self.current_token  
                res.register_advancement()
                self.advance()
                
                if self.current_token.type != 'CLOSINGPARENTHESIS':
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis"))  
                
                res.register_advancement()
                self.advance()
                
                return res.success(moveFaceNode(typeof, value))
            
            elif self.current_token.matches("NEGCONDITION"):
                    res.register_advancement()
                    self.advance()
                    
                    if self.current_token.type != "OPENPARENTHESIS":
                        return res.failure(InvalidSyntaxError(
                                self.current_token.pos_start, self.current_token.pos_end,
                                "Expected opening parenthesis"))  
                        
                    res.register_advancement()
                    self.advance()
                    
                    if "CONDITION" not in self.current_token.type:
                        return res.failure(InvalidSyntaxError(
                                self.current_token.pos_start, self.current_token.pos_end,
                                "Expected condition"))  
                    
                    condition = self.current_token
                    res.register_advancement()
                    self.advance()
                    
                    if self.current_token.type != "CLOSINGPARENTHESIS":
                        return res.failure(InvalidSyntaxError(
                                self.current_token.pos_start, self.current_token.pos_end,
                                "Expected closing parenthesis")) 
                        
                    res.register_advancement()
                    self.advance()
                    if self.current_token.type != "CLOSINGPARENTHESIS":
                        return res.failure(InvalidSyntaxError(
                                self.current_token.pos_start, self.current_token.pos_end,
                                "Expected opening parenthesis")) 

                    res.register_advancement()
                    self.advance()
                    return res.success(notConditional(condition))   
                     
            elif "CONDITION" in self.current_token.type:
                    if self.current_token.type == "FACINGCONDITION":
                        res.register_advancement()
                        condition = self.current_token
                        self.advance()
                        
                        if self.current_token.value not in [":north", ":south", ":east", ":west"]:
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected constant :north, :south, :west or :east.")) 

                        res.register_advancement()
                        self.advance()
                        if self.current_token.type != "CLOSINGPARENTHESIS":
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected closing parenthesis.")) 
                        res.register_advancement()
                        self.advance()                      
                        return res.success(conditional(condition))    
                    if self.current_token.type == "CANPUTCONDITION":
                        res.register_advancement()
                        condition = self.current_token
                        self.advance()
                        
                        if self.current_token.value not in [":balloons", ":chips"]:
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected constant :balloons or :chips.")) 

                        res.register_advancement()
                        self.advance()
                        
                        first = False
                        second = False
                        third = False
                        
                        if self.current_token.value not in globalVariables.keys():
                            first = True
                            
                        if self.current_token.type not in VALUE_CONSTANTS.values():
                            second = True
                            
                        if self.current_token.type != 'VALUE':
                            third = True
                            
                        if first and second and third:
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected either a variable, constant or value."))
                            
                        res.register_advancement()
                        self.advance()
                          
                        if self.current_token.type != "CLOSINGPARENTHESIS":
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected closing parenthesis.")) 
                        res.register_advancement()
                        self.advance()                      
                        return res.success(conditional(condition))   
                    if self.current_token.type == "CANPICKCONDITION":
                        res.register_advancement()
                        condition = self.current_token
                        self.advance()
                        
                        if self.current_token.value not in [":balloons", ":chips"]:
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected constant :balloons or :chips.")) 

                        res.register_advancement()
                        self.advance()
                        
                        first = False
                        second = False
                        third = False
                        
                        if self.current_token.value not in globalVariables.keys():
                            first = True
                            
                        if self.current_token.type not in VALUE_CONSTANTS.values():
                            second = True
                            
                        if self.current_token.type != 'VALUE':
                            third = True
                            
                        if first and second and third:
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected either a variable, constant or value."))
                            
                        res.register_advancement()
                        self.advance()
                          
                        if self.current_token.type != "CLOSINGPARENTHESIS":
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected closing parenthesis.")) 
                        res.register_advancement()
                        self.advance()                      
                        return res.success(conditional(condition))   
                    
                    if self.current_token.type == "CANMOVECONDITION":
                        res.register_advancement()
                        condition = self.current_token
                        self.advance()
                        
                        if self.current_token.value not in [":north", ":south", ":west", ":east"]:
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected constant :north, :south, :west, :east")) 

                        res.register_advancement()
                        self.advance()
                        
                        if self.current_token.type != "CLOSINGPARENTHESIS":
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected closing parenthesis.")) 
                        res.register_advancement()
                        self.advance()                      
                        return res.success(conditional(condition))
                    
                    if self.current_token.type == "ISZEROCONDITION":
                        res.register_advancement()
                        condition = self.current_token
                        self.advance()
                        
                        first = False
                        second = False
                        third = False
                        
                        if self.current_token.value not in globalVariables.keys():
                            first = True
                            
                        if self.current_token.type not in VALUE_CONSTANTS.values():
                            second = True
                            
                        if self.current_token.type != 'VALUE':
                            third = True
                            
                        if first and second and third:
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected either a variable, constant or value."))
                            
                        res.register_advancement()
                        self.advance()
                          
                        if self.current_token.type != "CLOSINGPARENTHESIS":
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected closing parenthesis.")) 
                        res.register_advancement()
                        self.advance()                      
                        return res.success(conditional(condition))    

                    if self.current_token.type == "BLOCKEDCONDITION":
                        res.register_advancement()
                        condition = self.current_token
                        self.advance()
                          
                        if self.current_token.type != "CLOSINGPARENTHESIS":
                            return res.failure(InvalidSyntaxError(
                                    self.current_token.pos_start, self.current_token.pos_end,
                                    "Expected closing parenthesis.")) 
                        res.register_advancement()
                        self.advance()                      
                        return res.success(conditional(condition))  


            elif self.current_token.matches('IF'):
                    res.register_advancement()
                    self.advance()

                    # Check for the opening parenthesis
                    if self.current_token.type != 'OPENPARENTHESIS':
                        return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected opening parenthesis after 'IF'"
                        ))

                    # Parse the condition
                    condition = res.register(self.expr())
                    if res.error:
                        return res

                    # Parse the true case
                    true_case = []
                    while not self.current_token.matches('CLOSINGPARENTHESIS'):
                        expr = res.register(self.expr())
                        if res.error:
                            return res
                        true_case.append(expr)
                        
                    res.register_advancement()
                    self.advance()

                    # Parse the else case
                    else_case = []
                    while not self.current_token.matches('CLOSINGPARENTHESIS'):
                        expr = res.register(self.expr())
                        if res.error:
                            return res
                        else_case.append(expr)

                    res.register_advancement()
                    self.advance()
                    # Check for the closing parenthesis for the else case
                    if self.current_token.type != 'CLOSINGPARENTHESIS':
                        return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected closing parenthesis for else case"
                        ))

                    res.register_advancement()
                    self.advance()

                    return res.success(IfNode(condition, true_case[0], else_case[-1]))           
            
        else:
            return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected opening parenthesis"))
            
        return res
                    
################################################3
def run(fn ,text):
    lexer = Lexer(fn, text)
    tokens = lexer.make_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    
    
    if ast.error: return None, ast.error
        
    return ast, ast.error