import sys
from lexer import do_lex
from nsparser import do_parse
from intepreter import Interpreter

def input_from_interpreter(var):
    value = input(f">> '{var}':")
    return value

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = do_lex(characters)
    # print(tokens)
    # print('\n\n')
    policy = do_parse(tokens)
    # print(policy)
    machine = Interpreter(policy, input_from_interpreter) 
    machine.process()