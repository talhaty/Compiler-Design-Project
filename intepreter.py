class Interpreter:
    def __init__(self, policy, input_callback=None):
        self.policy = policy
        self.stack = []
        self.variables = {}  # Grammar variable: varID -> varValue
        self.pos = 0
        self.input_callback = input_callback

    def stackEnd(self):
        if len(self.stack) >= 1:
            return self.stack[len(self.stack) - 1]
        else:
            return (None, None)

    def process(self):
        while self.pos < len(self.policy):
            self.stack.append(self.policy[self.pos])
            self.pos += 1

            if self.stackEnd()[1] == "#":
                self.pos = self.stack.pop()[0]
            elif self.stackEnd()[1] == "!F":
                adr = self.stack.pop()[0]
                if not self.stackEnd()[0]:
                    self.pos = adr
                self.stack.pop()
            elif self.stackEnd()[1] == "PRINT":
                self.stack.pop()
                self.printing(self.stack.pop()[0])
            elif self.stackEnd()[1] == "INPUT":
                self.stack.pop()
                self.inputting(self.stack.pop()[0])
            elif self.stackEnd() is not None:
                if not self.stackEnd()[1] in ["INT", "FLOAT", "BOOL", "ID", "STRING"]:
                    self.calculate()

    def printing(self, value):
        if self.variables.get(value) is not None:
            print("> " + str(self.variables.get(value)))
        else:
            print("> " + str(value))

    def inputting_(self, var):
        if self.variables.get(var) is not None:
            v = str(input(">>"))
            self.variables[var] = self.convertType(v)
        else:
            print("Error: variable '" + var + "' is undefined")
            
    def inputting(self, var):
        if self.variables.get(var) is not None:
            if self.input_callback:
                v = self.input_callback(var)
                self.variables[var] = self.convertType(v)
            else:
                print("Error: input callback not provided")
        else:
            print("Error: variable '" + var + "' is undefined")
            exit()

    def convertType(self, value):
        try:
            if value.find('"') != -1:
                return str(value)
            elif value.find('.') != -1:
                return float(value)
            else:
                return int(value)
        except:
            print("Error: unknown data type '" + value + "'")
            exit()
            

    def checkDef(self, var):
        if type(var) is tuple:
            if self.variables.get(var[0]) is None and var[1] == "ID":
                print("Error: variable '" + var[0] + "' is undefined")
                exit()
                

    def getValue(self, var):
        if var[1] == "INT":
            return int(var[0])
        elif var[1] == "FLOAT":
            return float(var[0])
        elif var[1] == "BOOL":
            return bool(var[0])
        else:
            return str(var[0])

    def calculate(self):
        
        op = self.stack.pop()[0]
        if self.stack == []:
            exit()
        if op not in ["++", "--", "!"]:
            b = self.stack.pop()
            a = self.stack.pop()
        else:
            a = self.stack.pop()
            b = (0, "INT")

        if op == "=":
            a = a[0]
            b = b[0] if b[1] == "ID" else self.getValue(b)
            self.assign(a, b)
        else:
            self.checkDef(a)
            self.checkDef(b)

            b = self.variables.get(b[0]) if self.variables.get(b[0]) is not None else self.getValue(b)
            if op == "++":
                self.inc(a[0])
            elif op == "--":
                self.dec(a[0])
            elif op == "-=":
                self.minusAssign(a[0], b)
            elif op == "+=":
                self.plusAssign(a[0], b)
            elif op == "*=":
                self.multAssign(a[0], b)
            elif op == "/=":
                self.divAssign(a[0], b)
            elif op == "//=":
                self.modAssign(a[0], b)
            else:
                a = self.variables.get(a[0]) if self.variables.get(a[0]) is not None else self.getValue(a)
                if op == ".":
                    self.stack.append(self.concat(a, b))
                elif op == "+":
                    self.stack.append(self.plus(a, b))
                elif op == "-":
                    self.stack.append(self.minus(a, b))
                elif op == "*":
                    self.stack.append(self.mult(a, b))
                elif op == "**":
                    self.stack.append(self.pow(a, b))
                elif op == "/":
                    self.stack.append(self.div(a, b))
                elif op == "//":
                    self.stack.append(self.mod(a, b))
                elif op == "and":
                    self.stack.append(self.l_and(a, b))
                elif op == "or":
                    self.stack.append(self.l_or(a, b))
                elif op == "xor":
                    self.stack.append(self.l_xor(a, b))
                elif op == ">":
                    self.stack.append(self.l_greater(a, b))
                elif op == ">=":
                    self.stack.append(self.l_greaterEq(a, b))
                elif op == "<":
                    self.stack.append(self.l_less(a, b))
                elif op == "<=":
                    self.stack.append(self.l_lessEq(a, b))
                elif op == "!=":
                    self.stack.append(self.l_notEq(a, b))
                elif op == "==":
                    self.stack.append(self.l_equal(a, b))
                elif op == "!":
                    self.stack.append(self.l_not(a))

    def concat(self, val1, val2):
        return str(val1) + str(val2), "STRING"

    def inc(self, var):
        self.variables[var] = self.variables.get(var) + 1

    def dec(self, var):
        self.variables[var] = self.variables.get(var) - 1

    def assign(self, num1, num2):
        self.variables[num1] = self.variables[num2] if self.variables.get(num2) is not None else num2

    def plus(self, num1, num2):
        if type(num1) == float or type(num2) == float:
            return num1 + num2, "FLOAT"
        else:
            return num1 + num2, "INT"

    def minus(self, num1, num2):
        if type(num1) == float or type(num2) == float:
            return (num1 - num2, "FLOAT")
        else:
            return (num1 - num2, "INT")

    def mult(self, num1, num2):
        if type(num1) == float or type(num2) == float:
            return num1 * num2, "FLOAT"
        else:
            return num1 * num2, "INT"

    def pow(self, num1, num2):
        res = num1 ** num2
        if type(res) == float:
            return res, "FLOAT"
        else:
            return res, "INT"

    def div(self, num1, num2):
        if num2 == 0:
            print("Error: division by zero !!!")
            exit()
            
        return float(num1) / float(num2), "FLOAT"

    def mod(self, num1, num2):
        if type(num1) == float or type(num2) == float:
            print("Error: modulus of float")
            exit()
            
        elif num2 == 0:
            print("Error: modulus by 0 -_-")
            exit()
            
        return num1 % num2, "INT"

    def minusAssign(self, var, num):
        self.variables[var] = self.variables.get(var) - num

    def plusAssign(self, var, num):
        self.variables[var] = self.variables.get(var) + num

    def multAssign(self, var, num):
        self.variables[var] = self.variables.get(var) * num

    def divAssign(self, var, num):
        if num != 0:
            self.variables[var] = self.variables.get(var) / float(num)
        else:
            print("Error: division by 0")
            exit()
            

    def modAssign(self, var, num):
        if type(self.variables.get(var)) != float and type(num) != float:
            print("Error: modulus by float -_-")
            exit()
            
        elif num == 0:
            print("Error: modulus by 0")
            exit()
            
        else:
            self.variables[var] = self.variables.get(var) % num

    def l_greater(self, num1, num2):
        try:
            return num1 > num2, "BOOL"
        except:
            self.compareException(num1, num2)

    def l_greaterEq(self, num1, num2):
        try:
            return num1 >= num2, "BOOL"
        except:
            self.compareException(num1, num2)

    def l_less(self, num1, num2):
        try:
            return num1 < num2, "BOOL"
        except:
            self.compareException(num1, num2)

    def l_lessEq(self, num1, num2):
        try:
            return num1 <= num2, "BOOL"
        except:
            self.compareException(num1, num2)

    def l_notEq(self, num1, num2):
        try:
            return num1 != num2, "BOOL"
        except:
            self.compareException(num1, num2)

    def l_equal(self, num1, num2):
        try:
            return num1 == num2, "BOOL"
        except:
            self.compareException(num1, num2)

    def l_not(self, num):
        if type(num) == bool:
            return not num, "BOOL"
        else:
            self.pushError("Error: using LOGICAL OR for non-logical expression")

    def l_or(self, num1, num2):
        if type(num1) == bool and type(num2) == bool:
            return num1 or num2, "BOOL"
        else:
            self.pushError("Error: using LOGICAL OR for non-logical expression")

    def l_and(self, num1, num2):
        if type(num1) == bool and type(num2) == bool:
            return num1 and num2, "BOOL"
        else:
            self.pushError("Error: using LOGICAL OR for non-logical expression")

    def l_xor(self, num1, num2):
        if type(num1) == bool and type(num2) == bool:
            return ((not num1) and num2) or ((num1 and (not num2))), "BOOL"
        else:
            self.pushError("Error: using LOGICAL OR for non-logical expression")

    def pushError(self, error):
        print(error)
        exit()
        

    def compareException(self, n1, n2):
        self.pushError("Error: impossible to compare '" +
                        str(n1) + "' and '" + str(n2) + "' values")



