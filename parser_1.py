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
           
class ifNode:
    def __init__(self, condition_node, body_node, else_body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        self.else_body_node = else_body_node
        
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end
        
    def __repr__(self):
        return f'{self.condition_node}, {self.body_node}, {self.else_body_node}'
    
class loopNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end
        
    def __repr__(self):
        return f'{self.condition_node}, {self.body_node}'
    
class repetTimesNode:
    def __init__(self, value_node, body_node):
        self.value_node = value_node
        self.body_node = body_node
        
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end
    def __repr__(self):
        return f'{self.value_node}, {self.body_node}'
    
class targetVariableNode:
    def __init__(self, variable_name_node, value_node):
        self.variable_name_node = variable_name_node
        self.value_node = value_node
        
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end
    def __repr__(self):
        return f'{self.variable_name_node}, {self.value_node}'
    
class varAccessNode:
    def __init__(self, var_name_node):
        self.var_name_node = var_name_node
        
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end
        
class valueNode:
    def __init__(self, value_node):
        self.value_node = value_node
        
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end
    def __repr__(self):
        return f'{self.value_node}'

class constantNode:
    def __init__(self, name_node):
        self.name_node = name_node
        
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end
    def __repr__(self):
        return f'{self.name_node}'
    
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
        self_token_index = -1
        self.advance()
        
    def advance(self, ):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token]
        return self.current_token
    
  def parse(self):
    res = self.expr()
    if not res.error and self.current_tok.type != TT_EOF:
      return res.failure(InvalidSyntaxError(
        self.current_tok.pos_start, self.current_tok.pos_end,
        "Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', <=', '>=', 'AND' or 'OR'"
      ))
    return res

        
        