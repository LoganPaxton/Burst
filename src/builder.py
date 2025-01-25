import sys
import burst

fp = sys.argv

try:
    cont = burst.importFile(fp[1])
    tokens = burst.parse(cont)
    burst.compile(tokens)
except IndexError:
    print("You need to provide a file when compiling Burst. (burst <file_name>)")
except FileNotFoundError:
    print(f"File {fp[1]} was not found at the provided path.")