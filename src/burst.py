# -----------
#   IMPORTS
# -----------

import re

# ---------------------
#   RUNTIME FUNCTIONS
# ---------------------

def read_file(file: str ) -> str:
    with open(file, "r") as f:
        return f.read()

# ------------- 
#   TOKENIZER
# -------------

def tokenize(code: str) -> list:
    tokens = []
    lines = code.strip().splitlines()

    for line in lines:

        if not line or line.startswith("#"):
            continue

        if line.startswith("print("):
            tokens.append(("PRINT", line))
        elif line.startswith("var"):
            tokens.append(("VAR", line))
        elif line.startswith("if"):
            tokens.append(("IF", line))
        else:
            tokens.append(("UNKNOWN", line))

    return tokens

# ------------
#   COMPILER
# ------------

def compiler(tokens: list) -> None:

    vars = {}

    for token_type, content in tokens:
        if token_type == "PRINT":
            match = re.match(r'print\(("([^"]*)"|[a-zA-Z_][a-zA-Z0-9_]*)\);', content)
            if match:
                val = match.group(1)
                if match.group(2) is not None:
                    print(match.group(2)) 
                else:
                    print(vars.get(val, f"Error: '{val}' is not defined"))
            else:
                print("COMPILE-TIME ERROR: Invalid print statement.")
        elif token_type == "VAR":
            match = re.match(r'var\s([a-zA-Z_][a-zA-Z0-9_]*)\s=\s(?:"([^"]*)"|input\(\));', content)
            if match:
                var = match.group(1)
                val = match.group(2)
                if val is not None:
                    vars[var] = val
                else:
                    vars[var] = input("")
            else:
                print("COMPILE-TIME ERROR: Syntax error in variable declaration.")
        elif token_type == "IF":
            match = re.match(r'if\s*\[\s*(?:"([^"]+)"|([A-Za-z_][A-Za-z0-9_]*))\s*(==|!=|<|>)\s*(?:"([^"]+)"|([A-Za-z_][A-Za-z0-9_]*))\s*\]\s*=>\s*\((.+)\);', content)
            if match:
                left = match.group(1) or vars.get(match.group(2), "")
                operator = match.group(3)
                right = match.group(4) or vars.get(match.group(5), "")
                body = match.group(6)

                if operator == "==" and left == right:
                    inner_tokens = tokenize(body)
                    compiler(inner_tokens)
                elif operator == "!=" and left != right:
                    inner_tokens = tokenize(body)
                    compiler(inner_tokens)
                elif operator == "<" and left < right:
                    inner_tokens = tokenize(body)
                    compiler(inner_tokens)
                elif operator == ">" and left > right:
                    inner_tokens = tokenize(body)
                    compiler(inner_tokens)
            else:
                print("COMPILE-TIME ERROR: Syntax error in if-statement.")