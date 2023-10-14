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
