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