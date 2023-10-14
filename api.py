import os


def getprop(name, path):
    with open(path, 'r', encoding='utf-8') as prop:
        for s in prop.readlines():
            if s[:1] == '#':
                continue
            if name in s:
                return s.strip().split('=')[1]
    return ''


def findfile(file, dir_) -> str:
    for root, dirs, files in os.walk(dir_, topdown=True):
        if file in files:
            if os.name == 'nt':
                return (root + os.sep + file).replace("\\", '/')
            else:
                return root + os.sep + file
        else:
            return ''
