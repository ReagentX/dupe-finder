import os
import pathlib
import hashlib


ROOT = '.'  # Just start at current folder for now
BUFFER_SIZE = 512 * 1024  # Size of a file to read into memory at once
hash_dict = {}  # Place to store our hashes and dates like { hex_digest: date, ..., }


def hash_file(path):
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def walk_from_path():
    files = os.scandir(ROOT)
    dirs = []
    for item in files:
        if item.is_dir():
            dirs.append(item)
        elif item.is_file():
            hash = hash_file(item.path)
            if hash in hash_dict:
                # Handle collision
                pass
            else:
                hash_dict[hash] = item.stat().st_birthtime
    print(dirs)
    print(hash_dict)

if __name__ == '__main__':
    walk_from_path()