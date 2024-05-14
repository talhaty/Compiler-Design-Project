
<h1 align="center">Code Interpreter</h1>



<p align="center">
  A simple code interpreter with a GUI built in Python.
</p>

## 🚀 Features

- **Syntax Checking**: Validate the syntax of your code before execution.
- **Code Execution**: Run your code directly within the interpreter.
- **Input Handling**: Support for input statements within the code.
- **Error Logging**: Display syntax and execution errors in the GUI.

## 🛠️ Installation and Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/talhaty/Compiler-Design-Project.git
   ```
   

2. Navigate to the project directory:

    ```bash
    cd code-interpreter
    ```


3. Run the application:

    ```bash
    #GUI
    python gui.py
    #CLI
    python main.py "codeFileName"
    ```

4. Write your code in the provided text box.

5. Click on the "Check Syntax" button to validate the syntax of your code.

6. Click on the "Execute" button to run your code.

7. If your code requires input, a prompt will appear to input the required values.

## 📜 Custom Language Grammar

The interpreter follows a custom language grammar, which includes the following components:
```
    lang -> expr*
    expr -> assign | if_stmt | printing | inputting
    assign -> var ((assign_op arif_stmt) | inc_dec) semicolon
    arif_stmt -> value (arif_op value)*
    value -> var | number | bkt_expr
    bkt_expr -> bkt_open arif_stmt bkt_close

    printing -> KW_PRINT bkt_open str_stmt bkt_close semicolon
    str_stmt -> substr (concat substr)*
    substr -> string | arif_stmt

    inputting -> KW_INPUT bkt_open var bkt_close semicolon

    if_stmt -> KW_IF bkt_open log_stmt bkt_close
                    brace_open expr* brace_close [else_stmt]
    else_stmt -> KW_ELSE brace_open expr* brace_close

    log_stmt -> comp_expr (log_op comp_expr)*
    comp_expr -> [log_not] (arif_stmt comp_op arif_stmt)

    KW_IF -> 'if'
    KW_ELSE -> 'else'
    KW_PRINT -> 'print'
    KW_INPUT -> 'input'

    bkt_open    -> (
    bkt_close   -> )
    brace_open  -> {
    brace_close -> }

    inc_dec -> ++ | --
    assign_op -> = | -= | += | *= | /= | //=
    arif_op -> * | ** | + | - | / | //
    comp_op -> < | <= | > | >= | != | ==
    log_op  -> 'or' | 'and' | 'xor'
    log_not -> 'not'

    string -> "[^"]*"
    var -> [A-Za-z_][A-Za-z_0-9]*
    number -> int | float | bool
    int -> -?[0-9]+
    float -> -?[0-9]+.[0-9]+
    bool -> True | False
    semicolon -> ";"
    concat -> "."
```

For more details on the grammar, refer to the grammar.txt file.
