import os
import shutil


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


def findfolder(dir__, folder_name, mh=0):
    for root, dirnames, filenames in os.walk(dir__):
        for dirname in dirnames:
            if mh == 1:
                if folder_name in dirname:
                    return os.path.join(root, dirname).replace("\\", '/')
            if dirname == folder_name:
                return os.path.join(root, dirname).replace("\\", '/')
    return None


def copy_folder(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for item in os.listdir(source_folder):
        source = os.path.join(source_folder, item)
        destination = os.path.join(destination_folder, item)

        if os.path.isdir(source):
            copy_folder(source, destination)
        else:
            shutil.copy2(source, destination)
