import hashlib

def read_file(file: str) -> str:
    with open(file, "r") as f:
        return f.read()

def calculate_sha256(file_path: str) -> hashlib.sha256:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()