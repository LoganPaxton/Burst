import re

def read_file(file: str) -> str:
    with open(file, "r") as f:
        return f.read()

def tokenize(code: str) -> list:
    tokens = []
    lines = code.strip().splitlines()

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith("print("):
            tokens.append(("PRINT", line))
        elif line.startswith("var"):
            tokens.append(("VAR", line))
        elif line.startswith("if"):
            tokens.append(("IF", line))
        elif re.match(r'[a-zA-Z_][a-zA-Z0-9_]*\s*[\+\-\*/]\s*[a-zA-Z0-9_"]+', line):
            tokens.append(("EXPR", line))
        else:
            tokens.append(("UNKNOWN", line))

    return tokens

def compiler(tokens: list) -> None:
    vars = {}

    for token_type, content in tokens:
        if token_type == "PRINT":
            match = re.match(
                r'print\((?:(?P<quoted>"[^"]*")|(?P<identifier>[a-zA-Z_][a-zA-Z0-9_]*)|i"(?P<interpolated>[^"]*)")\)\s*;?$',
                content
            )
            if match:
                if match.group("quoted") is not None:
                    print(match.group("quoted")[1:-1])
                elif match.group("identifier") is not None:
                    var_name = match.group("identifier")
                    print(vars.get(var_name, f"Error: '{var_name}' is not defined"))
                elif match.group("interpolated") is not None:
                    interpolated = match.group("interpolated")
                    for name, value in vars.items():
                        interpolated = interpolated.replace(f"${{{name}}}", value)
                    print(interpolated)
            else:
                print("COMPILE-TIME ERROR: Invalid print statement.")

        elif token_type == "VAR":
            match = re.match(
                r'var\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:"([^"]*)"|input\(\))\s*;?$',
                content
            )
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
            match = re.match(
                r'if\s*\[\s*(?:"([^"]*)"|([A-Za-z_][A-Za-z0-9_]*))\s*'
                r'(==|!=|<|>)\s*'
                r'(?:"([^"]*)"|([A-Za-z_][A-Za-z0-9_]*))\s*\]\s*'
                r'=>\s*\((.*?)\)'
                r'(?:\s*else\s*=>\s*\((.*?)\))?\s*;?$',
                content
            )
            if match:
                left = match.group(1) or vars.get(match.group(2), "")
                operator = match.group(3)
                right = match.group(4) or vars.get(match.group(5), "")
                if_body = match.group(6)
                else_body = match.group(7)

                condition_result = False
                if operator == "==":
                    condition_result = left == right
                elif operator == "!=":
                    condition_result = left != right
                elif operator == "<":
                    condition_result = left < right
                elif operator == ">":
                    condition_result = left > right

                body_to_run = if_body if condition_result else else_body
                if body_to_run:
                    inner_tokens = tokenize(body_to_run)
                    compiler(inner_tokens)

        elif token_type == "EXPR":
            match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*([\+\-\*/])\s*("?[a-zA-Z0-9_]+"?)', content)
            if match: 
                var_name, operator, value = match.groups()

                if var_name not in vars:
                    print(f"COMPILE-TIME ERROR: Variable '{var_name} is not defined.'")
                    continue
                
            if value.startswith('"') and value.endswith('"'):
                value = value.strip('"')
            elif value.isdigit():
                value = int(value)
            else:
                value = vars.get(value, 0)
            

            try:
                current = int(vars[var_name])
                val = int(value)
            except ValueError:
                print(f"COMPILE-TIME ERROR: Invalid arithmetic on non-integer values.")
                continue

            if operator == "+":
                vars[var_name] = str(current + val)
            elif operator == "-":
                vars[var_name] = str(current - val)
            elif operator == "*":
                vars[var_name] = str(current * val)
            elif operator == "/":
                vars[var_name] = str(current // val if val != 0 else 0)
        else:
            print("COMPILE-TIME ERROR: Syntax error in if-statement.")
