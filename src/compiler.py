import re
from tokenizer import tokenize
from utils import read_file
from exceptions import *


def compile(tokens: list, tokenize_func=None) -> None:
    if tokenize_func is None:
        tokenize_func = tokenize

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
                    if var_name not in vars:
                        raise UndefinedVariableError(var_name)
                    print(vars[var_name])
                elif match.group("interpolated") is not None:
                    interpolated = match.group("interpolated")
                    for name, value in vars.items():
                        interpolated = interpolated.replace(f"${{{name}}}", str(value))
                    print(interpolated)
            else:
                raise InvalidPrintStatement(value=content)

        elif token_type == "VAR":
            match = re.match(
                r'var\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:"([^"]*)"|input\(\)|(true|false)|([0-9]+))\s*;?$',
                content
            )
            if match:
                var = match.group(1)
                val = match.group(2)
                if val is not None:
                    vars[var] = val
                elif match.group(4) is not None:
                    vars[var] = int(match.group(4))
                elif match.group(3) is not None:
                    vars[var] = match.group(3) == "true"
                else:
                    vars[var] = input("")
            else:
                raise InvalidVarDeclaration(value=content)

        elif token_type == "IF":
            line = content.strip().rstrip(";")

            # Split IF and optional ELSE
            if " else => " in line:
                if_part, else_part = line.split(" else => ", 1)
                else_body = else_part.strip()[1:-1]  # remove ()
            else:
                if_part = line
                else_body = None

            # Parse IF
            if_part = if_part.replace("if", "", 1).strip()

            cond_part, then_part = if_part.split("=>", 1)
            cond_part = cond_part.strip()[1:-1]   # remove [ ]
            then_body = then_part.strip()[1:-1]   # remove ( )

            # Parse condition
            for op in ["==", "!=", ">=", "<=", ">", "<"]:
                if op in cond_part:
                    left_raw, right_raw = map(str.strip, cond_part.split(op))
                    operator = op
                    break
            else:
                raise InvalidConditional(content)

            # Resolve left operand
            if left_raw.startswith('"') and left_raw.endswith('"'):
                left = left_raw[1:-1]
            elif left_raw.isdigit():
                left = int(left_raw)
            else:
                if left_raw not in vars:
                    raise UndefinedVariableError(left_raw)
                left = vars[left_raw]


            # Resolve right operand
            if right_raw.startswith('"') and right_raw.endswith('"'):
                right = right_raw[1:-1]
            elif right_raw.isdigit():
                right = int(right_raw)
            else:
                if right_raw not in vars:
                    raise UndefinedVariableError(right_raw)
                right = vars[right_raw]


            # Evaluate condition
            try:
                if operator == "==":
                    condition_result = left == right
                elif operator == "!=":
                    condition_result = left != right
                elif operator == ">":
                    condition_result = left > right
                elif operator == "<":
                    condition_result = left < right
                elif operator == ">=":
                    condition_result = left >= right
                elif operator == "<=":
                    condition_result = left <= right
            except Exception as e:
                raise InvalidConditional(str(e))

            # Execute branch
            body_to_run = then_body if condition_result else else_body
            if body_to_run:
                inner_tokens = tokenize_func(body_to_run.strip())
                compile(inner_tokens, tokenize_func=tokenize_func)

        elif token_type == "EXPR":
            match = re.match(
                r'([a-zA-Z_][a-zA-Z0-9_]*)\s*([\+\-\*/])\s*(?:"([^"]*)"|([a-zA-Z_][a-zA-Z0-9_]*|\d+))\s*;?$',
                content.strip()
            )
            if match:
                var_name, operator, raw_str, raw_val = match.groups()

                if var_name not in vars:
                    raise UndefinedVariableError(var_name)

                if raw_str is not None:
                    raise ArithmeticStringError(value=raw_str)
                elif raw_val.isdigit():
                    value = int(raw_val)
                elif raw_val in vars:
                    value = vars[raw_val]
                    if not isinstance(value, int):
                        raise NonIntegerArithmeticError(var_name=raw_val)
                else:
                    raise InvalidExpressionSyntax(value=raw_val)

                current = vars[var_name]
                if not isinstance(current, int):
                    raise TargetNotIntegerError(var_name=var_name)

                if operator == "+":
                    vars[var_name] = current + value
                elif operator == "-":
                    vars[var_name] = current - value
                elif operator == "*":
                    vars[var_name] = current * value
                elif operator == "/":
                    vars[var_name] = current // value if value != 0 else 0
            else:
                raise InvalidExpressionSyntax(value=content)

        elif token_type == "INCLUDE":
            match = re.match(r'include\("([^"]+)"\)\s*;?$', content.strip())
            if match:
                include_path = match.group(1)
                try:
                    code = read_file(include_path)
                    included_tokens = tokenize_func(code)
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
                    raise FileNotFoundError(f"File '{include_path}' not found.")
            else:
                raise InvalidIncludeStatement(value=content)
            
        elif token_type == "FUNC":
            match = re.match(r'func\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((?P<args>[^)]*)\)\s*=>\s*\((?P<body>.*?)\)\s*;?$', content.strip())
            if match:
                func_name = match.group(1)
                args = match.group(2)
                body = match.group(3)

                vars[func_name] = {
                    "type": "function",
                    "params": [arg.strip() for arg in args.split(",") if arg.strip()],
                    "body": body
                }

        elif token_type == "UNKNOWN":
            call_match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*;?$', content.strip())
            
            if call_match:
                func_name = call_match.group(1)
                passed_args_raw = call_match.group(2)
                
                if func_name in vars:
                    definition = vars[func_name]
                    
                    is_func = isinstance(definition, dict) and definition.get("type") == "function"

                    if is_func:
                        local_vars = vars.copy()
                        inner_tokens = tokenize_func(definition.get("body"))
                        compile(inner_tokens, tokenize_func=tokenize_func)
                        return 
                    else:
                        raise InvalidCall()
                else:
                    raise UndefinedVariableError(func_name)
            
            else:
                raise InvalidExpressionSyntax(f"Unknown or invalid statement: {content}")
        
            