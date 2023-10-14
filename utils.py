import os
import subprocess
import zipfile
from os import getcwd
import platform as plat

elocal = getcwd()
platform = plat.machine()
ostype = plat.system()
binner = elocal + os.sep + "bin"
ebinner = binner + os.sep + ostype + os.sep + platform + os.sep


def call(exe, kz='Y', out=0, shstate=False, sp=0):
    if kz == "Y":
        cmd = f'{ebinner}{exe}'
    else:
        cmd = exe
    if os.name != 'posix':
        conf = subprocess.CREATE_NO_WINDOW
    else:
        if sp == 0:
            cmd = cmd.split()
        conf = 0
    try:
        ret = subprocess.Popen(cmd, shell=shstate, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, creationflags=conf)
        for i in iter(ret.stdout.readline, b""):
            if out == 0:
                print(i.decode("utf-8", "ignore").strip())
    except subprocess.CalledProcessError as e:
        for i in iter(e.stdout.readline, b""):
            if out == 0:
                print(e.decode("utf-8", "ignore").strip())
    ret.wait()
    return ret.returncode


def returnoutput(exe):
    cmd = f'{ebinner}{exe}'
    try:
        ret = subprocess.check_output(cmd, shell=False, stderr=subprocess.STDOUT)
        return ret.decode()
    except subprocess.CalledProcessError as e:
        return e.decode()


class setting:
    def __init__(self, file):
        self.set_f = file

    def get(self, vn):
        with open(self.set_f, 'r', encoding='utf-8') as f:
            for v in f.readlines():
                if v[:1] == '#':
                    continue
                if vn in v:
                    data = v.strip().split('=')[1].split()
                    if data.__len__() == 1:
                        return data[0]
                    else:
                        return data


class String:
    def __init__(self):
        self.var = None

    def set(self, v):
        setattr(self, 'var', v)

    def get(self):
        return self.var


def is_file_in_zip(zip_file_path, file_name):
    # 打开zip文件
    with zipfile.ZipFile(zip_file_path, 'r') as zf:
        # 获取zip文件中的所有文件名
        file_names = zf.namelist()
        # 判断指定文件名是否存在于zip文件中
        if file_name in file_names:
            return True
        else:
            return False


def extra_payload(file, out):
    with zipfile.ZipFile(file, 'r') as zf:
        zf.extract('payload.bin', out)
