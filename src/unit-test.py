import unittest
import re
from unittest.mock import patch, mock_open
from burst import tokenize, compiler

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

        if re.match(r'^print\((?:".*"|[a-zA-Z_][a-zA-Z0-9_]*|i".*")\)\s*;?$', line):
            tokens.append(("PRINT", line))
        elif line.startswith("var"):
            tokens.append(("VAR", line))
        elif line.startswith("if"):
            tokens.append(("IF", line))
        elif re.match(r'[a-zA-Z_][a-zA-Z0-9_]*\s*[\+\-\*/]\s*[a-zA-Z0-9_\"]+', line):
            tokens.append(("EXPR", line))
        elif line.startswith("include("):
            tokens.append(("INCLUDE", line))
        elif line.startswith("export("):
            tokens.append(("EXPORT", line))
        else:
            tokens.append(("UNKNOWN", line))

    return tokens

def compiler(tokens: list) -> None:
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
                    compiler(inner_tokens)

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

class TestCompilerFunctions(unittest.TestCase):

    def test_read_file(self):
        with patch("builtins.open", mock_open(read_data="sample data")) as mock_file:
            self.assertEqual(read_file("dummy.txt"), "sample data")
            mock_file.assert_called_once_with("dummy.txt", "r")

    def test_tokenize(self):
        code = """
        # This is a comment
        print("Hello, World");
        var x = 5;
        if [x == 5] => (print("x is five"));
        x + 1;
        include("file.txt");
        """
        expected_tokens = [
            ("PRINT", 'print("Hello, World");'),
            ("VAR", "var x = 5;"),
            ("IF", 'if [x == 5] => (print("x is five"));'),
            ("EXPR", "x + 1;"),
            ("INCLUDE", 'include("file.txt");'),
        ]
        self.assertEqual(tokenize(code), expected_tokens)

    def test_compiler_print_literal(self):
        tokens = [("PRINT", 'print("Hello, World");')]
        with patch('builtins.print') as mocked_print:
            compiler(tokens)
            mocked_print.assert_called_once_with("Hello, World")

    def test_compiler_print_undefined_variable(self):
        tokens = [("PRINT", 'print(unknownVar);')]
        with patch('builtins.print') as mocked_print:
            compiler(tokens)
            mocked_print.assert_called_once_with("Error: 'unknownVar' is not defined")

    def test_compiler_variable_declaration(self):
        tokens = [("VAR", 'var x = 10;'), ("PRINT", 'print(x);')]
        with patch('builtins.print') as mocked_print:
            compiler(tokens)
            mocked_print.assert_called_once_with(10)

    def test_compiler_if_statement_true(self):
        tokens = [("VAR", 'var x = 10;'), ("IF", 'if [x == 10] => (print("x is ten"));')]
        with patch('builtins.print') as mocked_print:
            compiler(tokens)
            mocked_print.assert_called_once_with("x is ten")

    def test_compiler_if_statement_false_with_else(self):
        tokens = [("VAR", 'var x = 10;'), ("IF", 'if [x == 5] => (print("x is five")) else => (print("x is not five"));')]
        with patch('builtins.print') as mocked_print:
            compiler(tokens)
            mocked_print.assert_called_once_with("x is not five")

    def test_compiler_invalid_expression(self):
        tokens = [("EXPR", 'x + "string";')]
        with patch('builtins.print') as mocked_print:
            compiler(tokens)
            mocked_print.assert_called_once_with("COMPILE-TIME ERROR: Arithmetic on string values is not allowed.")

    def test_compiler_include_file_not_found(self):
        tokens = [("INCLUDE", 'include("non_existent_file.txt");')]
        with patch('builtins.print') as mocked_print, patch('__main__.read_file', side_effect=FileNotFoundError):
            compiler(tokens)
            mocked_print.assert_called_once_with("INCLUDE ERROR: File 'non_existent_file.txt' not found.")

unittest.main(argv=[''], exit=False)
