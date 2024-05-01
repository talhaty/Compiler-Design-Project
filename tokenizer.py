import re

def tokenize_input(input_string):
    token_patterns = [
        (r'print|input|=', 'KEYWORD'),      # Keywords
        (r'\+|-|\*|/', 'OPERATOR'),         # Operators
        (r'\d+', 'NUMBER'),                  # Numeric literals
        (r'"[^"]*"', 'STRING'),              # String literals
        (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),  # Identifiers (variables)
        (r'=', 'ASSIGNMENT')                 # Assignment operator
    ]
    
    tokens = []
    
    while input_string:
        matched = False
        for pattern, token_type in token_patterns:
            match = re.match(pattern, input_string)
            if match:
                tokens.append((match.group(0), token_type))
                input_string = input_string[match.end():].strip()
                matched = True
                break
        if not matched:
            raise SyntaxError("Invalid input: " + input_string)
    
    return tokens

def prompt_user():
    expression = input("Enter code: ")
    return expression

def main():
    try:
        expression = prompt_user()
        tokens = tokenize_input(expression)
        print("Tokens:", tokens)
    except SyntaxError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
