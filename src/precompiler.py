import os
from utils import calculate_sha256, read_file
from tokenizer import tokenize
from compiler import compile

CACHE_DIR = ".bcache"

def precompile(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    os.makedirs(CACHE_DIR, exist_ok=True)

    sha256 = calculate_sha256(file_path)
    if not sha256:
        return False

    cache_file = f"{CACHE_DIR}/{sha256}.txt"

    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cached_code = f.read()

        tokens = tokenize(cached_code)
        compile(tokens)
        return True

    source = read_file(file_path)
    tokens = tokenize(source)

    output_lines = []

    def capture_print(*args, **kwargs):
        output_lines.append(" ".join(map(str, args)))

    import builtins
    original_print = builtins.print
    builtins.print = capture_print

    try:
        compile(tokens)
    finally:
        builtins.print = original_print

    with open(cache_file, "w") as f:
        f.write("\n".join(output_lines))

    for line in output_lines:
        print(line)

    return False
