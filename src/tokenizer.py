import re

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
        elif line.startswith("func"):
            tokens.append(("FUNC", line))
        else:
            tokens.append(("UNKNOWN", line))

    return tokens