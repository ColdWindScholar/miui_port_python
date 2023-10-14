# miui_port project

# Only For V-A/B Device

# Based on Android 13

# Test Base ROM: Mi 10S (V14.0.6)

# Test Port ROM: Mi13、Mi13Pro、Mi13Ultra

# 底包和移植包为外部参数传入

import sys

import imgextractor
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
payload_list = []
for i in utils.returnoutput('payload-dumper-go -l PORTROM/payload.bin').split('\n')[6].split(','):
    payload_list.append(i.split(' (')[0].replace(' ', ''))
for part in PORT_PARTITION:
    if part in payload_list:
        Yellow(f"底包 [{part}.img] 重命名为 [{part}_bak.img]")
        shutil.move(f'BASEROM/images/{part}.img', f'BASEROM/images/{part}_bak.img')
        Yellow(f"正在分解底包 [{part}_bak.img]")
        if utils.gettype(f'BASEROM/images/{part}_bak.img') == 'ext':
            imgextractor.Extractor().main(f'BASEROM/images/{part}_bak.img',
                                          LOCAL + os.sep + "BASEROM" + os.sep + "images" + os.sep + part + "_bak",
                                          LOCAL + os.sep + "BASEROM")
        elif utils.gettype(f'BASEROM/images/{part}_bak.img') == 'erofs':
            utils.call(f'extract.erofs -i BASEROM/images/{part}_bak.img -o BASEROM/images/ -x')
            for i in [f'{part}_bak_fs_config', f'{part}_bak_file_contexts']:
                if os.path.exists('BASEROM/images/config/' + i):
                    shutil.move('BASEROM/images/config/' + i, 'BASEROM/config/' + i)
        if os.path.isdir('BASEROM/images/'+part+'_bak'):
            try:
                os.remove(f'BASEROM/images/{part}_bak.img')
            except:
                pass
        Yellow(f"正在提取移植包 [{part}] 分区")
        if utils.call(f'payload-dumper-go -p {part} -o BASEROM/images/ PORTROM/payload.bin') != 0:
            Error(f"提取移植包 [{part}] 分区时出错")
if os.path.isdir('PORTROM'):
    shutil.rmtree('PORTROM')
Green("开始提取逻辑分区镜像")
for pname in SUPERLIST:
    if os.path.isdir(f"BASEROM/images/{pname}.img"):
        Yellow(f'正在提取 {pname}.img')
        if utils.gettype(f'BASEROM/images/{pname}.img') == 'ext':
            imgextractor.Extractor().main(f'BASEROM/images/{pname}.img',
                                          LOCAL + os.sep + "BASEROM" + os.sep + "images" + os.sep + pname,
                                          LOCAL + os.sep + "BASEROM")
        elif utils.gettype(f'BASEROM/images/{pname}.img') == 'erofs':
            utils.call(f'extract.erofs -i BASEROM/images/{pname}.img -o BASEROM/images/ -x')
            for i in [f'{pname}_fs_config', f'{pname}_file_contexts']:
                if os.path.exists('BASEROM/images/config/' + i):
                    shutil.move('BASEROM/images/config/' + i, 'BASEROM/config/' + i)
        if os.path.isdir('BASEROM/images/'+pname):
            try:
                os.remove(f'BASEROM/images/{pname}.img')
            except:
                pass
