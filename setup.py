import os
import platform

if platform.system() == 'Linux':
    if os.geteuid() != 0 and platform.machine() == 'x86_64':
        print("请以 root 用户运行")
        exit(1)
    if platform.machine() == 'x86_64':
        print("Device arch: x86_64")
        os.system('apt update -y')
        os.system('apt upgrade -y')
        if os.system('apt install -y aria2 python3 busybox zip unzip p7zip-full openjdk-8-jre') != 0:
            print("安装可能出错，请手动执行：apt install -y python3 busybox zip unzip p7zip-full")
    elif platform.machine() == 'aarch64':
        print('Device arch: aarch64')
        os.system('apt update -y')
        os.system('apt upgrade -y')
        os.system('apt install -y python busybox zip unzip p7zip openjdk-17')
