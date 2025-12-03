import re
import sys
from utils import read_file
from tokenizer import tokenize
from compiler import compile

if sys.argv[1] == "":
    print("The burst command requires an argument!")
    exit(0)

cont = read_file(sys.argv[1])
toks = tokenize(cont)
compile(toks)