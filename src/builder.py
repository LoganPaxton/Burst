import sys
import burst

fp = sys.argv

#print(fp)

try:
    cont = burst.read_file(fp[1])
    tokens = burst.tokenize(cont)
    burst.compiler(tokens)
except FileNotFoundError:
    print(f"File {fp[1]} was not found at the provided path.")
except IndexError:
    print("You need to provide a file when compiling Burst. (burst <file_name>)")