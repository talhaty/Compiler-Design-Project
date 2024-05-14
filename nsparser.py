from sys import exit

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens #set token after lexer
        self.pos = 0 #current token position
        self.policy = [] #reverse
        self.buffer = [] #stack 
        self.addrsForFilling  = [] #save the policy address
        self.addrsJumps  = [] #saves addresses (arrays) for jumps
        self.calls = [] 

    def parseExeption(self, expected, detected):
        print("\nParse error: detected " + "'" + detected + "', but " + "'" + expected + "' are expected!")
        exit(0)

    def endScript(self):
        return self.pos == len(self.tokens)

    def parse(self):
        return self.lang()

    #lang -> expr*
    def lang(self):
        while(not self.endScript()):
            if (not self.expr(self.pos)):
                self.parseExeption("expression", self.tokens[self.pos][0])
        return True    

    #expr -> assign | if_stmt
    def expr(self, pos):
        if not(
            self.assign(self.pos) or
            self.if_stmt(self.pos) or
            self.printing(self.pos) or
            self.inputting(self.pos)
            ):
            return False
        return True  

    #assign -> var ((assign_op arif_stmt) | inc_dec) semicolon
    def assign(self, pos):
        if (not self.var(self.pos)):
            return False
        if (self.assign_op(self.pos)):
            if (not self.arif_stmt(self.pos)):
                self.parseExeption("arithmetic expression", self.tokens[self.pos][0])
                return False
        elif (not self.inc_dec(self.pos)):
            self.parseExeption("=, ++ or --", self.tokens[self.pos][0])
            return False       
        if (not self.semicolon(self.pos)):
            self.parseExeption(";", self.tokens[self.pos][0])
            return False
        return True

    def var(self, pos):
        if self.tokens[self.pos][1] == "ID":
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False  

    def assign_op(self, pos):
        if (
            self.tokens[self.pos][1] == "ASSIGN" or
            self.tokens[self.pos][1] == "PLUS_ASSIGN" or
            self.tokens[self.pos][1] == "MINUS_ASSIGN" or
            self.tokens[self.pos][1] == "MULT_ASSIGN" or
            self.tokens[self.pos][1] == "DIVISION_ASSIGN" or
            self.tokens[self.pos][1] == "MOD_ASSIGN"
            ): 
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    #arif_stmt -> value (arif_op value)*
    def arif_stmt(self, pos):
        if (not self.value(self.pos)):
            return False
        while(True): #up gan up gan 
            if (not self.arif_op(self.pos) and not self.value(self.pos)):
                break   
        return True

    #value -> var | number | bkt_expr
    def value(self, pos):
        if not(
            self.var(self.pos)    or 
            self.number(self.pos) or
            self.bkt_expr(self.pos)
            ):
            return False
        return True 

    #number -> int | float | bool 
    def number(self, pos):
        if (
            self.tokens[self.pos][1] == "INT"   or
            self.tokens[self.pos][1] == "FLOAT" or
            self.tokens[self.pos][1] == "BOOL"
        ):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    #bkt_expr -> bkt_open arif_stmt bkt_close
    def bkt_expr(self, pos):
        if (not self.bkt_open(self.pos)):
            return False
        elif(not self.arif_stmt(self.pos)):
            self.parseExeption("arithmetic expression", self.tokens[self.pos][0])
            return False
        elif(not self.bkt_close(self.pos)):
            self.parseExeption(")", self.tokens[self.pos][0])
            return False
        return True

    #log_stmt -> comp_expr (log_op comp_expr)*
    def log_stmt(self, pos):
        if (not self.comp_expr(self.pos)):
            return False
        while(True): 
            if (self.log_op(self.pos)):
                if (not self.comp_expr(self.pos)):
                    self.parseExeption("compare expression", self.tokens[self.pos][0])
                    break
            else:
                break
        return True

    #comp_expr -> [log_not] (arif_stmt comp_op arif_stmt)
    def comp_expr(self, pos):
        if(self.log_not(self.pos)):
            pass
        if (self.arif_stmt(self.pos)):
            if(not self.comp_op(self.pos)):
                self.parseExeption("compare expression", self.tokens[self.pos][0])
                return False
            elif (not self.arif_stmt(self.pos)):
                self.parseExeption("", self.tokens[self.pos][0])
                return False
        else:
            return False
        return True    

    #if_stmt -> KW_IF bkt_open log_stmt bkt_close brace_open expr* brace_close [else_stmt]
    def if_stmt(self, pos):
        if (not self.KW_IF(self.pos)):
            return False
        elif(not self.bkt_open(self.pos)):
            self.parseExeption("(", self.tokens[self.pos][0])
            return False
        elif(not self.log_stmt(self.pos)):
            self.parseExeption("logical expression", self.tokens[self.pos][0])
            return False
        elif(not self.bkt_close(self.pos)):
            self.parseExeption(")", self.tokens[self.pos][0])
            return False
        elif(not self.brace_open(self.pos)):
            self.parseExeption("{", self.tokens[self.pos][0])
            return False
        while(True): 
            if (not self.expr(self.pos)):
                break     
        if(not self.brace_close(self.pos)):
            self.parseExeption("}", self.tokens[self.pos][0])
            return False
        if (self.tokens[self.pos][1] == "ELSE"):
            if (not self.else_stmt(self.pos)):
                return False
        return True

    #else_stmt -> KW_ELSE brace_open expr* brace_close
    def else_stmt(self, pos):
        if (not self.KW_ELSE(self.pos)):
            return False
        elif(not self.brace_open(self.pos)):
            self.parseExeption("{", self.tokens[self.pos][0])
            return False
        while(True): 
            if (not self.expr(self.pos)):
                break   
        if(not self.brace_close(self.pos)):
            self.parseExeption("}", self.tokens[self.pos][0])
            return False
        return True    

    def KW_IF(self, pos):
        if (self.tokens[self.pos][1] == "IF"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def KW_ELSE(self, pos):
        if (self.tokens[self.pos][1] == "ELSE"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False  

    #printing -> KW_PRINT bkt_open arif_stmt bkt_close semicolon
    def printing(self, pos):
        if (not self.KW_PRINT(self.pos)):
            return False
        elif (not self.bkt_open(self.pos)):
            self.parseExeption("(", self.tokens[self.pos][0])
            return False
        elif (not self.str_stmt(self.pos)):
            self.parseExeption("string or arithmetic expressions", self.tokens[self.pos][0])
            return False
        elif (not self.bkt_close(self.pos)):
            self.parseExeption(")", self.tokens[self.pos][0])
            return False
        elif (not self.semicolon(self.pos)):
            self.parseExeption(";", self.tokens[self.pos][0])
            return False
        else:
            return True
    
    def KW_PRINT(self, pos):
        if (self.tokens[self.pos][1] == "PRINT"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    #str_stmt -> substr (concat substr)*
    def str_stmt(self, pos):
        if (not self.substr(self.pos)):
            return False
        while(True): #up gan up gan 
            if (not self.concat(self.pos) and not self.substr(self.pos)):
                break   
        return True

    #substr -> string | arif_stmt
    def substr(self, pos):
        if (
            self.string(self.pos) or
            self.arif_stmt(self.pos)
        ):
            return True
        else:
            return False

    def string(self, pos):
        if (self.tokens[self.pos][1] == "STRING"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False  

    def concat(self, pos):
        if (self.tokens[self.pos][1] == "CONCAT"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    #inputting -> KW_INPUT bkt_open var bkt_close semicolon
    def inputting(self, pos):
        if (not self.KW_INPUT(self.pos)):
            return False
        elif (not self.bkt_open(self.pos)):
            self.parseExeption("(", self.tokens[self.pos][0])
            return False
        elif (not self.var(self.pos)):
            self.parseExeption("variable", self.tokens[self.pos][0])
            return False
        elif (not self.bkt_close(self.pos)):
            self.parseExeption(")", self.tokens[self.pos][0])
            return False
        elif (not self.semicolon(self.pos)):
            self.parseExeption(";", self.tokens[self.pos][0])
            return False
        else:
            return True

    def KW_INPUT(self, pos):
        if (self.tokens[self.pos][1] == "INPUT"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def brace_open(self, pos):
        if (self.tokens[self.pos][1] == "BRACE_OPEN"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False 

    def brace_close(self, pos):
        if (self.tokens[self.pos][1] == "BRACE_CLOSE"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False     

    def bkt_open(self, pos):
        if (self.tokens[self.pos][1] == "BRACKET_OPEN"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def bkt_close(self, pos):
        if (self.tokens[self.pos][1] == "BRACKET_CLOSE"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False         
    
    #increment and decrement functions
    def inc_dec(self, pos):
        if (
            self.tokens[self.pos][1] == "INC" or
            self.tokens[self.pos][1] == "DEC" 
        ):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
        return True

    def arif_op(self, pos):
        if (
            self.tokens[self.pos][1] == "MULT"        or
            self.tokens[self.pos][1] == "PLUS"        or
            self.tokens[self.pos][1] == "MINUS"       or
            self.tokens[self.pos][1] == "DIVISION"    or
            self.tokens[self.pos][1] == "MOD"         or
            self.tokens[self.pos][1] == "POW"
        ):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def log_op(self, pos):
        if (
            self.tokens[self.pos][1] == "AND" or
            self.tokens[self.pos][1] == "OR"  or
            self.tokens[self.pos][1] == "XOR"       
        ):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def comp_op(self, pos):
        if (
            self.tokens[self.pos][1] == "GRATER_EQ"  or
            self.tokens[self.pos][1] == "GRATER"     or
            self.tokens[self.pos][1] == "LESS_EQ"    or
            self.tokens[self.pos][1] == "LESS"       or 
            self.tokens[self.pos][1] == "EQUAL"      or
            self.tokens[self.pos][1] == "NOT_EQUAL"
        ):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def log_not(self, pos):
        if (self.tokens[self.pos][1] == "NOT"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True
        else:
            return False

    def semicolon(self, pos):
        if (self.tokens[pos][1] == "SEMICOLON"):
            self.pushInStack(self.tokens[self.pos])
            self.pos += 1
            return True        
        else:
            return False

    # If the input token is a number, variable, or conditional selection
    # add to common stack or reserved stack 
    # sort by priority token
    def pushInStack(self, el):
        #print(self.policy)
        #print(str(self.buffer) + "\n====")
        if (el[1] in 
        ["INT", "FLOAT", "BOOL", "ID", "STRING"]):
            self.policy.append( (el[0], el[1]) )
        elif (el[1] in ["IF", "ELSE"]):
            self.calls.append(el[1])
            self.buffer.append(el)
            if (el[1] in  ["ELSE"]):
                self.buffer.pop()
                self.addrsForFilling.append( len(self.policy) )
                self.policy.append ( 0 ) 

        else:  
            if (el[0] == ")"):#push to buffer
                while (self.endEl(self.buffer)[0] != "("):
                    value = self.buffer.pop()
                    self.policy.append( (value[0], value[1]))
                self.buffer.pop()
                if (self.endEl(self.buffer)[1] in ["IF"]):
                        self.buffer.pop()
                        self.addrsForFilling.append( len(self.policy) )
                        self.policy.append ( 0 ) 
            elif (el[0] == "}"): 
                while (self.endEl(self.buffer)[0] != "{"):
                    value = self.buffer.pop()
                    self.policy.append( (value[0], value[1]))
                self.buffer.pop()
                lastCall = self.calls.pop()
                if (lastCall == "IF"):
                    self.policy[self.addrsForFilling.pop()] = (len(self.policy) + 1, "!F") 
                elif (lastCall == "ELSE"):
                    self.policy[self.addrsForFilling.pop()] = (len(self.policy), "!")
                else:
                    
                    self.policy.append( (None, None) )           
            elif (el[0] != "(" and el[0] != "{" and len(self.buffer) != 0):
                
            
                if (el[2] < self.endEl(self.buffer)[2]):                 
                    if (el[1] == "SEMICOLON"):
                        
                        while (not self.endEl(self.buffer)[0] in
                        ["=", "-=", "+=", "*=", "/=", "//=", "++", "--", "print", ".", "input"]):
                            val = self.buffer.pop()
                            self.policy.append( (val[0], val[1]) )
                    val = self.buffer.pop() 
                    self.policy.append( (val[0], val[1]) )

            if (not el[0] in [";", ")", "}"]):
                self.buffer.append(el)   
    
    def endEl(self, n):
        try:
            return n[len(n) - 1]
        except:
            return (None, None)

def do_parse(tokens):
    p = Parser(tokens)
    if (p.parse()):
        return p.policy