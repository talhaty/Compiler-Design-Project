import re

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

class Tokenizer:
    def __init__(self):
        self.token_patterns = [
            (r'print|input', 'KEYWORD'),      # Keywords
            (r'\+|-|\*|/', 'OPERATOR'),         # Operators
            (r'\d+', 'NUMBER'),                  # Numeric literals
            (r'"[^"]*"', 'STRING'),              # String literals
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),  # Identifiers (variables)
            (r'=', 'ASSIGNMENT')                 # Assignment operator
        ]

    def tokenize_input(self, input_string):
        tokens = []
        input_string = self.remove_comments(input_string)
        
        while input_string:
            matched = False
            for pattern, token_type in self.token_patterns:
                match = re.match(pattern, input_string)
                if match:
                    tokens.append(Token(token_type, match.group(0)))
                    input_string = input_string[match.end():].strip()
                    matched = True
                    break
            if not matched:
                raise SyntaxError("Invalid input: " + input_string)
        
        return tokens

    def remove_comments(self, input_string):
        # Regular expression to match comments and whitespace
        comment_pattern = r'#.*?$'
        return re.sub(comment_pattern, '', input_string, flags=re.MULTILINE)
