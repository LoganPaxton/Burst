import re
import sys
from utils import read_file
from tokenizer import tokenize
from compiler import compile
from precompiler import precompile

if len(sys.argv) < 2:
    print("The burst command requires an argument!")
    exit(1)

file_path = sys.argv[1]

cache_used = precompile(file_path)

cont = read_file(file_path)
toks = tokenize(cont)
compile(toks)