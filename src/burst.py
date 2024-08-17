import re


class ASTNode:
  pass


class VariableDeclaration(ASTNode):

  def __init__(self, name, initializer):
    self.name = name
    self.initializer = initializer


class PrintStatement(ASTNode):

  def __init__(self, expression, interpolate=False):
    self.expression = expression
    self.interpolate = interpolate


class InputStatement(ASTNode):

  def __init__(self, prompt, var_name):
    self.prompt = prompt
    self.var_name = var_name


def tokenize(code):
  # Improved regex to handle floats as single tokens
  tokens = re.findall(r'\b\w+\b|[=()]|i?\"[^\"]*\"|\d*\.\d+|\d+', code)
  #print("Tokens:", tokens)  # Debug: Print tokens
  return tokens


def parse(tokens):
  if len(tokens) >= 4 and tokens[0].lower() == "var" and tokens[2] == "=":
    if tokens[3].lower() == "prompt":
      # Extract prompt text which is enclosed in parentheses
      prompt_tokens = tokens[4:-1]  # Exclude 'prompt' and parentheses
      prompt_text = " ".join(prompt_tokens).strip().strip('"')
      return InputStatement(prompt_text, tokens[1])
    else:
      name = tokens[1]
      initializer = parse_initializer(" ".join(
          tokens[3:]))  # Concatenate tokens
      return VariableDeclaration(name, initializer)
  elif len(tokens) == 5 and tokens[0].lower(
  ) == 'print' and tokens[1] == '(' and tokens[4] == ')':
    if tokens[2] == 'i' and tokens[3].startswith('"') and tokens[3].endswith(
        '"'):
      expression = tokens[3][1:-1]  # Remove the quotes
      return PrintStatement(expression, interpolate=True)
    elif tokens[2].startswith('"') and tokens[2].endswith('"'):
      expression = tokens[2][1:-1]  # Remove the quotes
      return PrintStatement(expression)
    else:
      raise RuntimeError("Invalid Syntax")
  else:
    raise RuntimeError("Invalid Syntax")


def parse_initializer(value):
  """Parse the initializer value and return the correct type."""
  value = value.strip()
  if value.startswith('"') and value.endswith('"'):
    return value[1:-1]  # Remove the quotes and return as string
  value = value.replace(' ', '')  # Remove spaces for number parsing
  try:
    return int(value)
  except ValueError:
    try:
      return float(value)
    except ValueError:
      raise RuntimeError("Invalid initializer value")


class Interpreter:

  def __init__(self):
    self.variables = {}

  def visit(self, node):
    if isinstance(node, VariableDeclaration):
      self.visit_variable_declaration(node)
    elif isinstance(node, PrintStatement):
      self.visit_print_statement(node)
    elif isinstance(node, InputStatement):
      self.visit_input_statement(node)

  def visit_variable_declaration(self, node):
    # Store the value as is, whether it's a string, number, or float
    self.variables[node.name] = node.initializer

  def visit_print_statement(self, node):
    expression = node.expression
    if node.interpolate:
      # Replace variables in the string
      for var_name, var_value in self.variables.items():
        expression = expression.replace(f"{{{var_name}}}", str(var_value))
    print(expression)

  def visit_input_statement(self, node):
    user_input = input(node.prompt)
    # Try to convert user input to int or float if possible
    try:
      value = int(user_input)
    except ValueError:
      try:
        value = float(user_input)
      except ValueError:
        value = user_input
    self.variables[node.var_name] = value


# Read and process code
with open('main.br') as file:
  code = file.readlines()

if not code:
  exit()

interpreter = Interpreter()

for line in code:
  tokens = tokenize(line.strip())
  if tokens:
    ast = parse(tokens)
    interpreter.visit(ast)
