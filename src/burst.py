import re

def importFile(e: str) -> str:
    with open(e, "r", encoding="utf-8") as file:
        return file.read()

def parse(e: str) -> list:
    tokens = []
    lines = e.split("\n")
    # Patterns for different statements
    printPattern = re.compile(r'print\("([^"]*)"\);', re.IGNORECASE)
    variablePattern = re.compile(r'var\s([A-Za-z_][A-Za-z0-9_]*)\s=\s"([^"]*)";', re.IGNORECASE)
    printVarPattern = re.compile(r'print\(([A-Za-z_][A-Za-z0-9_]*)\);', re.IGNORECASE)
    interpolatedPattern = re.compile(r'print\(i"([^"]*)"\);', re.IGNORECASE)
    promptPattern = re.compile(r'var\s([A-Za-z_][A-Za-z0-9_]*)\s=\sprompt\("([^"]*)"\);', re.IGNORECASE)

    for i in lines:
        # Ignore comments
        i = i.strip()
        if i.startswith("#"):
            continue

        # Match print statements with strings
        printMatch = re.match(printPattern, i)
        if printMatch:
            tokens.append("print")
            tokens.append("openParen")
            tokens.append("quoteOpen")
            tokens.append(printMatch.group(1))  # Extract string inside quotes
            tokens.append("quoteClose")
            tokens.append("closeParen")
            tokens.append("semicolon")
            continue

        # Match variable declarations
        variableMatch = re.match(variablePattern, i)
        if variableMatch:
            tokens.append("varKeyword")
            tokens.append(variableMatch.group(1))  # Variable name
            tokens.append("equals")
            tokens.append("quoteOpen")
            tokens.append(variableMatch.group(2))  # Variable value
            tokens.append("quoteClose")
            tokens.append("semicolon")
            continue

        # Match print statements with variables
        printVarMatch = re.match(printVarPattern, i)
        if printVarMatch:
            tokens.append("print")
            tokens.append("openParen")
            tokens.append("variableName")
            tokens.append(printVarMatch.group(1))  # Variable name
            tokens.append("closeParen")
            tokens.append("semicolon")
            continue

        # Match interpolated print statements
        interpolatedMatch = re.match(interpolatedPattern, i)
        if interpolatedMatch:
            tokens.append("print")
            tokens.append("openParen")
            tokens.append("interpolated")
            tokens.append(interpolatedMatch.group(1))  # Full interpolated string
            tokens.append("quoteClose")
            tokens.append("closeParen")
            tokens.append("semicolon")
            continue

        # Match variable declarations with prompt
        promptMatch = re.match(promptPattern, i)
        if promptMatch:
            tokens.append("varKeyword")
            tokens.append(promptMatch.group(1))  # Variable name
            tokens.append("equals")
            tokens.append("prompt")
            tokens.append("openParen")
            tokens.append("quoteOpen")
            tokens.append(promptMatch.group(2))  # Prompt message
            tokens.append("quoteClose")
            tokens.append("closeParen")
            tokens.append("semicolon")
            continue

    return tokens

def compile(tokens: list) -> None:
    variables = {}  # Dictionary to store variables and their values
    i = 0
    while i < len(tokens):
        if tokens[i] == "print":
            # Handle print statements
            if (
                i + 6 < len(tokens) and
                tokens[i + 1] == "openParen" and
                tokens[i + 2] == "quoteOpen" and
                tokens[i + 4] == "quoteClose" and
                tokens[i + 5] == "closeParen" and
                tokens[i + 6] == "semicolon"
            ):
                # Print string literal
                print(tokens[i + 3])
                i += 7
            elif (
                i + 5 < len(tokens) and
                tokens[i + 1] == "openParen" and
                tokens[i + 2] == "variableName" and
                tokens[i + 4] == "closeParen" and
                tokens[i + 5] == "semicolon"
            ):
                # Print variable value
                var_name = tokens[i + 3]
                if var_name in variables:
                    print(variables[var_name])
                else:
                    print(f"Error: Undefined variable '{var_name}'")
                i += 6
            elif (
                i + 6 < len(tokens) and
                tokens[i + 1] == "openParen" and
                tokens[i + 2] == "interpolated" and
                tokens[i + 4] == "quoteClose" and
                tokens[i + 5] == "closeParen" and
                tokens[i + 6] == "semicolon"
            ):
                # Print interpolated string
                interpolated_string = tokens[i + 3]
                interpolated_value = interpolated_string

                # Replace variables in the string
                for var_name in variables:
                    placeholder = f"${{{var_name}}}"
                    if placeholder in interpolated_string:
                        interpolated_value = interpolated_value.replace(placeholder, variables[var_name])

                print(interpolated_value)
                i += 7
            else:
                print("Syntax error in print statement.")
                break
        elif tokens[i] == "varKeyword":
            # Handle variable declarations
            if (
                i + 6 < len(tokens) and
                tokens[i + 2] == "equals" and
                tokens[i + 3] == "quoteOpen" and
                tokens[i + 5] == "quoteClose" and
                tokens[i + 6] == "semicolon"
            ):
                var_name = tokens[i + 1]
                var_value = tokens[i + 4]
                variables[var_name] = var_value  # Store the variable and its value
                i += 7
            # Handle variable declarations with prompt
            elif (
                i + 9 < len(tokens) and
                tokens[i + 2] == "equals" and
                tokens[i + 3] == "prompt" and
                tokens[i + 4] == "openParen" and
                tokens[i + 5] == "quoteOpen" and
                tokens[i + 7] == "quoteClose" and
                tokens[i + 8] == "closeParen" and
                tokens[i + 9] == "semicolon"
            ):
                var_name = tokens[i + 1]
                prompt_message = tokens[i + 6]
                user_input = input(prompt_message + " ")  # Display prompt and get user input
                variables[var_name] = user_input
                i += 10
            else:
                print("Syntax error in variable declaration.")
                break
        else:
            print(f"Unexpected token: {tokens[i]}")
            break
