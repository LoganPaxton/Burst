import os
import sys
from utils import calculate_sha256, read_file
from tokenizer import tokenize
from compiler import compile

CACHE_DIR = ".bcache"

import os
import sys
from contextlib import redirect_stdout

def save_cache(file_path):
    sha256 = calculate_sha256(file_path)

    cache_path = os.path.join(CACHE_DIR, f"{sha256}.txt")
    os.makedirs(CACHE_DIR, exist_ok=True)

    with open(cache_path, "w") as f:
        with redirect_stdout(f):
            cont = read_file(file_path)
            toks = tokenize(cont)
            compile(toks)
            
    return cache_path

def precompile(file_path):

    sha256 = calculate_sha256(file_path)

    if not os.path.exists(f"{CACHE_DIR}/{sha256}.txt"):
        return False

    cont = read_file(f"{CACHE_DIR}/{sha256}.txt")
    content = cont.split("\n")

    for i in content:
        if i == "":
            continue
        print(i.strip())
    
    return True