import unittest
import re
from unittest.mock import patch, mock_open
from utils import read_file
from tokenizer import tokenize
from compiler import compile
from exceptions import InvalidPrintStatement, UndefinedVariableError, ArithmeticStringError, TargetNotIntegerError, InvalidExpressionSyntax, InvalidVarDeclaration, InvalidConditional


class TestCompilerFunctions(unittest.TestCase):

    def test_read_file(self):
        with patch("builtins.open", mock_open(read_data="sample data")) as mock_file:
            self.assertEqual(read_file("dummy.txt"), "sample data")
            mock_file.assert_called_once_with("dummy.txt", "r")

    def test_tokenize(self):
        code = """
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

    def test_compile_print_literal(self):
        tokens = [("PRINT", 'print("Hello, World");')]
        with patch('builtins.print') as mocked_print:
            compile(tokens)
            mocked_print.assert_called_once_with("Hello, World")

    def test_compile_variable_declaration(self):
        tokens = [("VAR", 'var x = 10;'), ("PRINT", 'print(x);')]
        with patch('builtins.print') as mocked_print:
            compile(tokens)
            mocked_print.assert_called_once_with(10)

    def test_compile_if_statement_true(self):
        tokens = [("VAR", 'var x = 10;'), ("IF", 'if [x == 10] => (print("x is ten"));')]
        with patch('builtins.print') as mocked_print:
            compile(tokens)
            mocked_print.assert_called_once_with("x is ten")

    def test_compile_if_statement_false_with_else(self):
        tokens = [("VAR", 'var x = 10;'), ("IF", 'if [x == 5] => (print("x is five")) else => (print("x is not five"));')]
        with patch('builtins.print') as mocked_print:
            compile(tokens)
            mocked_print.assert_called_once_with("x is not five")

    def test_compile_print_undefined_variable_raises_exception(self):
        tokens = [("PRINT", 'print(unknownVar);')]
        with self.assertRaises(UndefinedVariableError) as cm:
            compile(tokens)
        self.assertEqual(cm.exception.value, 'unknownVar')

    def test_compile_invalid_expression_arithmetic_on_string_raises_exception(self):
        tokens = [("VAR", 'var x = 10;'), ("EXPR", 'x + "string";')]
        with self.assertRaises(ArithmeticStringError):
            compile(tokens)

    def test_compile_expression_target_not_int_raises_exception(self):
        tokens = [("VAR", 'var s = "hello";'), ("EXPR", 's + 5;')]
        with self.assertRaises(TargetNotIntegerError) as cm:
            compile(tokens)
        self.assertEqual(cm.exception.value, 's')

    def test_compile_invalid_var_declaration_raises_exception(self):
        tokens = [("VAR", 'var 1x = 10;')]
        with self.assertRaises(InvalidVarDeclaration):
            compile(tokens)

    def test_compile_include_file_not_found_raises_exception(self):
        tokens = [("INCLUDE", 'include("non_existent_file.txt");')]
        with self.assertRaises(FileNotFoundError):
            with patch('utils.read_file', side_effect=FileNotFoundError):
                compile(tokens)


if __name__ == '__main__':
    unittest.main()