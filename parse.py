from tokenizer import Token, Tokenizer

class Node:
    def __str__(self):
        return "Node"

class StatementNode(Node):
    pass

class ExpressionNode(Node):
    pass

class BinaryOperationNode(ExpressionNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"BinaryOperationNode({self.left}, {self.operator}, {self.right})"

class NumberNode(ExpressionNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"NumberNode({self.value})"

class StringNode(ExpressionNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"StringNode({self.value})"

class IdentifierNode(ExpressionNode):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"IdentifierNode({self.name})"

class PrintStatementNode(StatementNode):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f"PrintStatementNode({self.expression})"

class InputStatementNode(StatementNode):
    def __init__(self, prompt):
        self.prompt = prompt

    def __str__(self):
        return f"InputStatementNode({self.prompt})"
    
class AssignmentStatementNode(StatementNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __str__(self):
        return f"AssignmentStatementNode({self.identifier}, {self.value})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = 0
        self.variables = {}

    def parse(self):
        self.advance()
        return self.parse_statement()

    def advance(self):
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            self.index += 1
        else:
            self.current_token = None

    def match(self, expected_type):
        if self.current_token and self.current_token.token_type == expected_type:
            self.advance()
        else:
            raise SyntaxError("Unexpected token: {}".format(self.current_token.value))

    def parse_statement(self):
        if self.current_token.token_type == 'IDENTIFIER':
            identifier = self.current_token.value
            self.match('IDENTIFIER')  

            if self.current_token.token_type == 'ASSIGNMENT':
                self.match('ASSIGNMENT')  
                value = self.parse_expression() 
                self.variables[identifier] = value
                
                return AssignmentStatementNode(identifier, value)
            else:
                raise SyntaxError("Invalid statement")
        elif self.current_token.token_type == 'KEYWORD':
            if self.current_token.value == 'print':
                return self.parse_print_statement()
            elif self.current_token.value == 'input':
                return self.parse_input_statement()
        else:
            raise SyntaxError("Invalid statement")

    def parse_print_statement(self):
        self.match('KEYWORD')  # 'print'
        expression = self.parse_expression()
        return PrintStatementNode(expression)

    def parse_input_statement(self):
        self.match('KEYWORD')  # 'input'
        prompt = self.current_token.value
        self.match('STRING')  # string prompt
        return InputStatementNode(prompt)

    def parse_expression(self):
        return self.parse_binary_operation() 

    def parse_binary_operation(self):
        left = self.parse_primary()
        while self.current_token and self.current_token.token_type == 'OPERATOR':
            operator = self.current_token.value
            self.match('OPERATOR')
            right = self.parse_primary()
            left = BinaryOperationNode(left, operator, right)
        return left

    def parse_primary(self):
        if self.current_token.token_type == 'NUMBER':
            value = self.current_token.value
            self.match('NUMBER')
            return NumberNode(value)
        elif self.current_token.token_type == 'STRING':
            value = self.current_token.value
            self.match('STRING')
            return StringNode(value)
        elif self.current_token.token_type == 'IDENTIFIER':
            name = self.current_token.value

            # Check if variable is defined
            if name not in self.variables:
                raise SyntaxError(f"Variable '{name}' is not defined")

            self.match('IDENTIFIER')
            return IdentifierNode(name)
        else:
            raise SyntaxError("Invalid expression")

if __name__ == "__main__":
    input_string = "a=1+1"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize_input(input_string)
    print("TOKENS:")
    for token in tokens:
        print(f"({token.value}, {token.token_type}) ", end=" ")
    print("\n\nPARSE TREE:")
    parser = Parser(tokens)
    parse_tree = parser.parse()
    print(parse_tree)
