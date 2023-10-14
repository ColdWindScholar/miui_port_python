from time import strftime


def LOG(info):
    print('[%s] %s\n' % (strftime('%H:%M:%S'), info))


def LOGI(info):
    print('[%s] \033[94m[INFO]\033[0m%s\n' % (strftime('%H:%M:%S'), info))


def Error(info):
    print('[%s] \033[91m%s\033[0m\n' % (strftime('%H:%M:%S'), info))


def Yellow(info):
    print('[%s] \033[93m%s\033[0m\n' % (strftime('%H:%M:%S'), info))


def Green(info):
    print('[%s] \033[92m%s\033[0m\n' % (strftime('%H:%M:%S'), info))
