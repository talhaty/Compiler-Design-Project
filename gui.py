import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from io import StringIO
from lexer import do_lex
from nsparser import do_parse
from intepreter import Interpreter
import sys
sys.stdout = StringIO()
sys.stderr = StringIO()
class CodeInterpreterApp:
    def __init__(self, master):
        self.master = master
        master.title("Code Interpreter")

        self.code_text = scrolledtext.ScrolledText(master, width=50, height=10, wrap=tk.WORD)
        self.code_text.pack(pady=10)

        self.check_syntax_button = tk.Button(master, text="Check Syntax", command=self.check_syntax)
        self.check_syntax_button.pack()

        self.execute_button = tk.Button(master, text="Execute", command=self.execute_code)
        self.execute_button.pack()

        self.error_logger = scrolledtext.ScrolledText(master, width=50, height=5, wrap=tk.WORD, state=tk.DISABLED, fg="red")
        self.error_logger.pack(pady=10)

        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

    def check_syntax(self):
        code = self.code_text.get("1.0", tk.END)
        try:
            tokens = do_lex(code)
            do_parse(tokens)
            self.error_logger.config(state=tk.NORMAL)
            self.error_logger.delete("1.0", tk.END)
            self.error_logger.insert(tk.END, "Syntax is correct!")
            self.error_logger.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Syntax Error: {str(e)}")
        

    def execute_code(self):
        code = self.code_text.get("1.0", tk.END)
        try:
            tokens = do_lex(code)
            policy = do_parse(tokens)
            machine = Interpreter(policy, self.input_from_interpreter) 

            # Capture the output first
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            machine.process()
            output = sys.stdout.getvalue()

            # Then update the error logger with the output
            self.error_logger.config(state=tk.NORMAL)
            self.error_logger.delete("1.0", tk.END)
            self.error_logger.insert(tk.END, output)
            self.error_logger.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Execution Error: {str(e)}")

        

    def input_from_interpreter(self, var):
        value = simpledialog.askstring("Input", f">> '{var}':")
        return value


    def convertType(self, value):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

def main():
    root = tk.Tk()
    app = CodeInterpreterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
