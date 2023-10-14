# miui_port project

# Only For V-A/B Device

# Based on Android 13

# Test Base ROM: Mi 10S (V14.0.6)

# Test Port ROM: Mi13、Mi13Pro、Mi13Ultra

# 底包和移植包为外部参数传入

import sys
from log import Error, Yellow, Green
import os
import utils
import downloader
import shutil

LOCAL = os.getcwd()
BASEROM = sys.argv[1]
PORTROM = sys.argv[2]

setting = utils.setting(os.path.join(LOCAL, 'bin', 'port_config'))
# 移植的分区，可在 bin/port_config 中更改
PORT_PARTITION = setting.get('partition_to_port')
SUPERLIST = setting.get('super_list')
REPACKEXT4 = setting.get("repack_with_ext4")
if not os.path.exists(BASEROM) and 'http' in BASEROM:
    Yellow('底包为一个链接，正在尝试下载')
    try:
        downloader.download([BASEROM], LOCAL)
    except:
        if os.path.exists(os.path.basename(BASEROM)):
            try:
                os.remove(os.path.basename(BASEROM))
            except:
                pass
        Error("底包下载错误！")
        sys.exit(1)
elif os.path.exists(BASEROM):
    Green(f"底包: {BASEROM}")
else:
    Error("底包参数错误")
    sys.exit(1)

if not os.path.exists(PORTROM) and 'http' in PORTROM:
    Yellow('移植包为一个链接，正在尝试下载')
    try:
        downloader.download([PORTROM], LOCAL)
    except:
        if os.path.exists(os.path.basename(PORTROM)):
            try:
                os.remove(os.path.basename(PORTROM))
            except:
                pass
        Error("移植包下载错误！")
        sys.exit(1)
elif os.path.exists(PORTROM):
    Green(f"移植包: {PORTROM}")
else:
    Error("移植包参数错误")
    sys.exit(1)
BASEROM = os.path.basename(BASEROM)
PORTROM = os.path.basename(PORTROM)
deviceCode = utils.String()
if "miui_" in BASEROM:
    deviceCode.set(BASEROM.split('_')[1])
else:
    deviceCode.set("YourDevice")
Yellow("正在检测ROM包")
if not utils.is_file_in_zip(BASEROM, 'payload.bin'): Error("底包没有payload.bin，请用MIUI官方包作为底包")
if not utils.is_file_in_zip(PORTROM, 'payload.bin'): Error("目标移植包没有payload.bin，请用MIUI官方包作为底包")
Green("ROM初步检测通过")
Yellow("正在清理文件")
for i in PORT_PARTITION:
    if os.path.isdir(os.path.join(LOCAL, i)):
        try:
            shutil.rmtree(os.path.join(LOCAL, i))
        except:
            pass
for i in ['app', 'config', 'BASEROM', 'PORTROM']:
    if os.path.isdir(os.path.join(LOCAL, i)):
        try:
            shutil.rmtree(os.path.join(LOCAL, i))
        except:
            pass
    elif os.path.isfile(os.path.join(LOCAL, i)):
        try:
            os.remove(os.path.join(LOCAL, i))
        except:
            pass

for root, dirs, files in os.walk(LOCAL):
    for d in dirs:
        if d.startswith('PORT_'):
            directory_path = os.path.join(root, d)
            shutil.rmtree(directory_path)
for i in ['BASEROM/images/', 'BASEROM/config/', 'PORTROM/images/']:
    os.makedirs(i)
Green("文件清理完毕")
Yellow("正在提取底包 [payload.bin]")
try:
    utils.extra_payload(BASEROM, 'BASEROM')
except:
    Error("解压底包 [payload.bin] 时出错")
    sys.exit(1)
Green("底包 [payload.bin] 提取完毕")
Yellow("正在提取移植包 [payload.bin]")
try:
    utils.extra_payload(PORTROM, 'PORTROM')
except:
    Error("解压移植包 [payload.bin] 时出错")
    sys.exit(1)
Green("移植包 [payload.bin] 提取完毕")
Yellow("开始分解底包 [payload.bin]")
if utils.call("payload-dumper-go -o BASEROM/images/ BASEROM/payload.bin") != 0:
    Error("分解底包 [payload.bin] 时出错")
    sys.exit(1)
for part in PORT_PARTITION:
