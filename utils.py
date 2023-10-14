import zipfile


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
