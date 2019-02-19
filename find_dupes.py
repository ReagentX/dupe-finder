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

def walk_from_path(path=ROOT):
    files = os.scandir(path)
    dirs = []
    dupes = []
    for item in files:
        if item.is_dir():
            dirs.append(item)
        elif item.is_file():
            hash = hash_file(item.path)
            if hash in hash_dict:
                print(f'Collision!', item.path)
                if item.stat().st_birthtime > hash_dict[hash][0]:
                    print('This version is newer than the one in the dict; add to dupes list')
                    dupes.append(item.path)
                elif item.stat().st_birthtime < hash_dict[hash][0]:
                    print('The earlier seen version is newer; add that to the dupes list')
                    dupes.append(hash_dict[hash][1])
                    hash_dict[hash] = (item.stat().st_birthtime, item.path)
                pass
            else:
                hash_dict[hash] = (item.stat().st_birthtime, item.path)
    for dir in dirs:
        walk_from_path(dir)
    return dupes

if __name__ == '__main__':
    data = walk_from_path()
    print(data, file='out.txt')