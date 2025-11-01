import os


def convert_path(path):
    if path == '~' or path.startswith('~'):
        path = os.path.expanduser(path)
    elif path == '.':
        path = os.getcwd()
    elif not path.startswith('/') and not path.startswith('..'):
        path = os.path.join(os.getcwd(), path)
    return path
