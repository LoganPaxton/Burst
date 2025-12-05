class CompilerError(Exception):
    """Base class for all custom compiler exceptions."""
    def __init__(self, message="Compiler error", value=None, line=None):
        self.message = message
        self.value = value
        self.line = line  # Optional: to indicate the line number where the error occurred
        super().__init__(self.message)

    def __str__(self):
        msg = self.message
        if self.value is not None:
            # Note: Changed to f-string with standard formatting
            msg += f": {self.value}"
        if self.line is not None:
            msg = f"[Line {self.line}] " + msg
        return msg

# --- Print Statement Errors ---

class InvalidPrintStatement(CompilerError):
    """Raised for general syntax errors in a print statement."""
    def __init__(self, value=None, line=None):
        super().__init__("Invalid print statement syntax", value, line)

class UndefinedVariableError(CompilerError):
    """Raised when an identifier in a print statement is not defined."""
    def __init__(self, var_name, line=None):
        super().__init__(f"Undefined variable", var_name, line)


# --- Variable Declaration Errors ---

class InvalidVarDeclaration(CompilerError):
    """Raised for syntax errors in variable declarations."""
    def __init__(self, value=None, line=None):
        super().__init__("Syntax error in variable declaration", value, line)


# --- Expression/Arithmetic Errors ---

class InvalidExpressionSyntax(CompilerError):
    """Raised for general syntax errors in an arithmetic expression."""
    def __init__(self, value=None, line=None):
        super().__init__("Invalid expression syntax", value, line)

class ArithmeticStringError(CompilerError):
    """Raised when arithmetic is attempted on a string literal/variable."""
    def __init__(self, value=None, line=None):
        super().__init__("Arithmetic on string values is not allowed", value, line)

class NonIntegerArithmeticError(CompilerError):
    """Raised when arithmetic is attempted with a non-integer variable."""
    def __init__(self, var_name, line=None):
        super().__init__(f"Cannot perform arithmetic with non-integer value", var_name, line)

class TargetNotIntegerError(CompilerError):
    """Raised when the target variable in an expression is not an integer."""
    def __init__(self, var_name, line=None):
        super().__init__(f"Target variable is not an integer", var_name, line)


# --- Include Errors ---

class InvalidIncludeStatement(CompilerError):
    """Raised for syntax errors in an include statement."""
    def __init__(self, value=None, line=None):
        super().__init__("Invalid include statement syntax", value, line)

# --- General/Catch-all Errors ---

class InvalidConditional(CompilerError):
    """Raised for general issues during conditional (if statement) evaluation."""
    def __init__(self, error_details=None, line=None):
        super().__init__("Failed conditional evaluation", error_details, line)

class InvalidFunctionDefinition(CompilerError):
    """Raised for general issues during function statement evaluation."""
    def __init__(self, error_details=None, line=None):
        super().__init__("Failed function evaluation", error_details, line)

class InvalidCall(CompilerError):
    """Line was not a valid function call (i.e. function without a declaration)."""
    def __init__(self, error_details=None, line=None):
        super().__init__("Invalid call", error_details, line)