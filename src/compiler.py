import re
from tokenizer import tokenize
from utils import read_file

def compile(tokens: list) -> None:
    vars = {}

    for token_type, content in tokens:
        if token_type == "PRINT":
            match = re.match(
                r'print\((?:"(?P<quoted>[^"]*)"|(?P<identifier>[a-zA-Z_][a-zA-Z0-9_]*)|i"(?P<interpolated>[^"]*)")\)\s*;?$',
                content.strip()
            )
            if match:
                if match.group("quoted") is not None:
                    print(match.group("quoted"))
                elif match.group("identifier") is not None:
                    var_name = match.group("identifier")
                    print(vars.get(var_name, f"Error: '{var_name}' is not defined"))
                elif match.group("interpolated") is not None:
                    interpolated = match.group("interpolated")
                    for name, value in vars.items():
                        interpolated = interpolated.replace(f"${{{name}}}", str(value))
                    print(interpolated)
            else:
                print("COMPILE-TIME ERROR: Invalid print statement.")

        elif token_type == "VAR":
            match = re.match(
                r'var\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:"([^"]*)"|input\(\)|(true|false)|([0-9]+))\s*;?$',
                content
            )
            if match:
                var = match.group(1)
                val = match.group(2)
                if val is not None:
                    vars[var] = val  # string
                elif match.group(4) is not None:
                    vars[var] = int(match.group(4))  # int
                elif match.group(3) is not None:
                    vars[var] = match.group(3) == "true"  # bool
                else:
                    vars[var] = input("")
            else:
                print("COMPILE-TIME ERROR: Syntax error in variable declaration.")

        elif token_type == "IF":
            match = re.match(
                r'if\s*\[\s*(?:"([^"]*)"|([A-Za-z_][A-Za-z0-9_]*))\s*'
                r'(==|!=|<|>|>=|<=)\s*'
                r'(?:"([^"]*)"|([A-Za-z_][A-Za-z0-9_]*))\s*\]\s*'
                r'=>\s*\((.*?)\)'
                r'(?:\s*else\s*=>\s*\((.*?)\))?\s*;?$',
                content.strip()
            )
            if match:
                left_raw = match.group(1)
                left_var = match.group(2)
                operator = match.group(3)
                right_raw = match.group(4)
                right_var = match.group(5)
                if_body = match.group(6)
                else_body = match.group(7)

                left = left_raw if left_raw is not None else vars.get(left_var, "")
                right = right_raw if right_raw is not None else vars.get(right_var, "")

                condition_result = False
                try:
                    if operator == "==":
                        condition_result = left == right
                    elif operator == "!=":
                        condition_result = left != right
                    elif operator == "<":
                        condition_result = left < right
                    elif operator == ">":
                        condition_result = left > right
                    elif operator == ">=":
                        condition_result = left >= right
                    elif operator == "<=":
                        condition_result = left <= right
                except Exception as e:
                    print(f"COMPILE-TIME ERROR: Failed condition evaluation: {e}")
                    continue

                body_to_run = if_body if condition_result else else_body
                if body_to_run:
                    inner_tokens = tokenize(body_to_run.strip())
                    compile(inner_tokens)

        elif token_type == "EXPR":
            match = re.match(
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s*([\+\-\*/])\s*(?:"([^"]*)"|([a-zA-Z_][a-zA-Z0-9_]*|\d+))\s*;?$',
                content.strip()
            )
            if match:
                var_name, operator, raw_str, raw_val = match.groups()

                if var_name not in vars:
                    print(f"COMPILE-TIME ERROR: Variable '{var_name}' is not defined.")
                    continue

                if raw_str is not None:
                    print("COMPILE-TIME ERROR: Arithmetic on string values is not allowed.")
                    continue
                elif raw_val.isdigit():
                    value = int(raw_val)
                elif raw_val in vars:
                    value = vars[raw_val]
                    if not isinstance(value, int):
                        print(f"COMPILE-TIME ERROR: Cannot perform arithmetic with non-integer '{raw_val}'.")
                        continue
                else:
                    print(f"COMPILE-TIME ERROR: Unknown variable or invalid number '{raw_val}'.")
                    continue

                current = vars[var_name]
                if not isinstance(current, int):
                    print(f"COMPILE-TIME ERROR: Variable '{var_name}' is not an integer.")
                    continue

                if operator == "+":
                    vars[var_name] = current + value
                elif operator == "-":
                    vars[var_name] = current - value
                elif operator == "*":
                    vars[var_name] = current * value
                elif operator == "/":
                    vars[var_name] = current // value if value != 0 else 0
            else:
                print("COMPILE-TIME ERROR: Invalid expression syntax.")

        elif token_type == "INCLUDE":
            match = re.match(r'include\("([^"]+)"\)\s*;?$', content.strip())
            if match:
                include_path = match.group(1)
                try:
                    code = read_file(include_path)
                    included_tokens = tokenize(code)
                    exported_vars = {}
                    for ttype, tcontent in included_tokens:
                        if ttype == "EXPORT":
                            export_match = re.match(r'export\(var\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*"([^"]*)"\)', tcontent)
                            if export_match:
                                var_name = export_match.group(1)
                                var_value = export_match.group(2)
                                exported_vars[var_name] = var_value
                    vars.update(exported_vars)
                except FileNotFoundError:
                    print(f"INCLUDE ERROR: File '{include_path}' not found.")
            else:
                print("COMPILE-TIME ERROR: Invalid include statement.")
