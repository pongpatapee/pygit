import os
import hashlib
import zlib


def read_file(path):
    with open(path, "rb") as f:
        return f.read()


def write_file(path, data):
    with open(path, "wb") as f:
        f.write(data)


def init(repo):
    os.mkdir(repo)
    os.mkdir(os.path.join(repo, ".git"))

    for name in ["objects", "refs", "refs/head"]:
        os.mkdir(os.path.join(repo, ".git", name))

    write_file(os.path.join(repo, ".git", "HEAD"), b"ref: refs/heads/main")

    print(f"initialized empty repository {repo}")


def hash_object(data, obj_type, write=True):
    header = f"{obj_type} {len(data)}".encode()
    full_data = header + b"\x00" + data

    sha1 = hashlib.sha1(full_data).hexdigest()

    if write:
        path = os.path.join(".git", "objects", sha1[:2], sha1[2:])
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            write_file(path, zlib.compress(full_data))

    return sha1
