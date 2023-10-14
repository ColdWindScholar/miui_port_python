def getprop(name, path):
    with open(path, 'r', encoding='utf-8') as prop:
        for s in prop.readlines():
            if s[:1] == '#':
                continue
            if name in s:
                return s.strip().split('=')[1]
    return ''
