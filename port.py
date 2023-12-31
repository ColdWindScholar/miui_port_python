# miui_port project
import re
# Only For V-A/B Device

# Based on Android 13

# Test Base ROM: Mi 10S (V14.0.6)

# Test Port ROM: Mi13、Mi13Pro、Mi13Ultra

# 底包和移植包为外部参数传入

import sys
import zipfile

import imgextractor
from api import getprop, findfile, findfolder, copy_folder
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
packType = utils.String()
packType.set('ext4')
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
            if REPACKEXT4 != 'true':
                packType.set('erofs')
            utils.call(f'extract.erofs -i BASEROM/images/{part}_bak.img -o BASEROM/images/ -x')
            for i in [f'{part}_bak_fs_config', f'{part}_bak_file_contexts']:
                if os.path.exists('BASEROM/images/config/' + i):
                    shutil.move('BASEROM/images/config/' + i, 'BASEROM/config/' + i)
        if os.path.isdir('BASEROM/images/' + part + '_bak'):
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
        if os.path.isdir('BASEROM/images/' + pname):
            try:
                os.remove(f'BASEROM/images/{pname}.img')
            except:
                pass
        Green(f"提取 [{pname}] 镜像完毕")
Yellow("正在获取ROM参数")
base_android_version = getprop('ro.vendor.build.version.release', 'BASEROM/images/vendor/build.prop')
port_android_version = getprop("ro.system.build.version.release", 'BASEROM/images/system/system/build.prop')
Green(f"安卓版本: 底包为[Android {base_android_version}], 移植包为 [Android {port_android_version}]")
base_android_sdk = getprop("ro.vendor.build.version.sdk", 'BASEROM/images/vendor/build.prop')
port_android_sdk = getprop("ro.system.build.version.sdk", 'BASEROM/images/system/system/build.prop')
Green(f"SDK 版本: 底包为 [SDK {base_android_sdk}], 移植包为 [SDK {port_android_sdk}]")
base_rom_version = getprop("ro.vendor.build.version.incremental", 'BASEROM/images/vendor/build.prop')
port_rom_version = getprop("ro.system.build.version.incremental", 'BASEROM/images/system/system/build.prop')
Green(f"ROM 版本: 底包为 [{base_rom_version}], 移植包为 [{port_rom_version}]")
base_miui_version = getprop("ro.miui.ui.version.code", 'BASEROM/images/product_bak/etc/build.prop')
port_miui_version = getprop("ro.miui.ui.version.code", 'BASEROM/images/product/etc/build.prop')
Green(f"MIUI版本: 底包为 [{base_miui_version}], 移植包为 [{port_miui_version}]")
base_rom_code = getprop("ro.product.vendor.device", 'BASEROM/images/vendor/build.prop')
port_rom_code = getprop("ro.product.system.device", 'BASEROM/images/system/system/build.prop')
Green(f"机型代号: 底包为 [{base_rom_code}], 移植包为 [{port_rom_code}]")
base_rom_marketname = getprop("ro.product.vendor.marketname", 'BASEROM/images/vendor/build.prop')
port_rom_marketname = getprop("ro.product.system.marketname", 'BASEROM/images/system/system/build.prop')  # 这个很可能是空的
Green(f"机型名称: 底包为 [{base_rom_marketname}], 移植包为 [{port_rom_marketname}]")
Yellow("去除avb校验")
for root, dirs, files in os.walk('BASEROM/images/'):
    for f in files:
        if f.startswith('fstab.'):
            with open(os.path.join(root, f), 'r') as f_:
                data = f_.readlines()
            with open(os.path.join(root, f), 'w', encoding='utf-8') as f_:
                data = [re.sub(r',avb_keys=.*avbpubkey', '', i) for i in data]
                data = [i.replace(',avb=vbmeta_system', '') for i in data]
                data = [i.replace(',avb=vbmeta_vendor', '') for i in data]
                data = [i.replace(',avb=vbmeta', '') for i in data]
                data = [i.replace(',avb', '') for i in data]
                f_.writelines(data)
remove_data_encrypt = setting.get("remove_data_encryption")
if remove_data_encrypt == 'ture':
    Yellow("去除data加密")
    for root, dirs, files in os.walk('BASEROM/images/'):
        for f in files:
            if f.startswith('fstab.'):
                Yellow(f"Target: {f}")
                with open(os.path.join(root, f), 'r') as f_:
                    data = f_.readlines()
                with open(os.path.join(root, f), 'w', encoding='utf-8') as f_:
                    data = [
                        i.replace(',fileencryption=aes-256-xts:aes-256-cts:v2+inlinecrypt_optimized+wrappedkey_v0', '')
                        for i in data]
                    data = [i.replace(',fileencryption=aes-256-xts:aes-256-cts:v2+emmc_optimized+wrappedkey_v0', '') for
                            i in data]
                    data = [i.replace(',fileencryption=aes-256-xts:aes-256-cts:v2', '') for i in data]
                    data = [i.replace(',metadata_encryption=aes-256-xts:wrappedkey_v0', '') for i in data]
                    data = [i.replace(',fileencryption=aes-256-xts:wrappedkey_v0', '') for i in data]
                    data = [i.replace(',metadata_encryption=aes-256-xts', '') for i in data]
                    data = [i.replace(',fileencryption=aes-256-xts', '') for i in data]
                    data = [i.replace('fileencryption', 'encryptable') for i in data]
                    data = [i.replace(',fileencryption=ice', '') for i in data]
                    f_.writelines(data)
for i in ["AospFrameworkResOverlay.apk", "MiuiFrameworkResOverlay.apk", "AospWifiResOverlay.apk",
          "DevicesAndroidOverlay.apk", "DevicesOverlay.apk", "MiuiBiometricResOverlay.apk"]:
    base = findfile(i, 'BASEROM/images/product_bak/')
    port = findfile(i, 'BASEROM/images/product/')
    if base and port and os.path.isfile(base) and os.path.exists(port):
        Yellow(f'正在替换 [{i}]')
        shutil.copy(base, port)
if os.path.isdir('BASEROM/images/product/etc/displayconfig/'):
    shutil.rmtree('BASEROM/images/product/etc/displayconfig')
    shutil.copytree('BASEROM/images/product_bak/etc/displayconfig', 'BASEROM/images/product/etc')
Yellow("正在替换 displayconfig")
Yellow("正在替换 device_features")
if os.path.isdir('BASEROM/images/product/etc/displayconfig/'):
    shutil.rmtree('BASEROM/images/product/etc/device_features')
    shutil.copytree('BASEROM/images/product_bak/etc/device_features', 'BASEROM/images/product/etc')
for d in ["MiuiCamera", "MiSound", 'MusicFX', "MiuiBiometric"]:
    base = findfolder("BASEROM/images/product_bak/", d)
    port = findfolder('BASEROM/images/product/', d)
    if not base and d == 'MusicFX':
        base = findfolder('BASEROM/images/system_bak/', d)
    if not port and d == 'MusicFX':
        base = findfolder('BASEROM/images/system/', d)
    if d == "MiuiBiometric":
        base = findfolder("BASEROM/images/product_bak/", d, mh=1)
        port = findfolder('BASEROM/images/product/', d, mh=1)
        if base and os.path.isdir(base) and not port:
            shutil.copytree(base, 'BASEROM/images/product/app/')
            continue
    if base and port and os.path.isdir(base) and os.path.exists(port):
        Yellow(f'正在替换 [{i}]')
        shutil.rmtree(port)
        shutil.copytree(base, os.path.dirname(port))
Yellow("正在修复 NFC")
if os.path.isdir('BASEROM/images/product_bak/pangu/system'):
    copy_folder('BASEROM/images/product_bak/pangu/system', 'BASEROM/images/system/')
if os.path.isfile('BASEROM/images/system_bak/system/etc/permissions/com.android.nfc_extras.xml') and os.path.isfile(
        'BASEROM/images/system/system/etc/permissions/com.android.nfc_extras.xml'):
    shutil.copy('BASEROM/images/system_bak/system/etc/permissions/com.android.nfc_extras.xml',
                'BASEROM/images/system/system/etc/permissions/com.android.nfc_extras.xml')
if os.path.isfile('BASEROM/images/system_bak/system/framework/com.android.nfc_extras.jar') and os.path.isfile(
        'BASEROM/images/system/system/framework/com.android.nfc_extras.jar'):
    shutil.copy('BASEROM/images/system_bak/system/framework/com.android.nfc_extras.jar',
                'BASEROM/images/system/system/framework/com.android.nfc_extras.jar')
frameworkjar = findfile('framework.jar', 'BASEROM/images/system/system')
if os.path.isfile(frameworkjar) and int(port_android_version) >= 13:
    Yellow("正在去除安卓应用签名限制")
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    with zipfile.ZipFile(frameworkjar, 'r') as zf:
        for i in zf.namelist():
            if i.endswith('.dex'):
                zf.extract(i, 'tmp')
    for i in os.listdir('tmp'):
        if i.endswith('.dex'):
            print(f'I: Baksmaling {i}')
            fname = i.split('.')[0]
            utils.call(
                f'java -jar bin/apktool/baksmali.jar d --api {port_android_sdk} {LOCAL + os.sep + "tmp" + os.sep + i} -o tmp/{fname}')
            os.remove(LOCAL + os.sep + "tmp" + os.sep + i)
    targetSmali = findfile('ApkSignatureVerifier.smali', 'tmp')
    if targetSmali and os.path.isfile(targetSmali):
        print(f'I: Target {targetSmali}')
        targetdir = os.path.basename(targetSmali)
        with open(targetSmali, 'r', encoding='utf-8') as f:
            data = f.readlines()
        with open(targetSmali, 'w', encoding='utf-8') as f:
            f.writelines([i.replace('const/4 v0, 0x2', 'const/4 v0, 0x1') for i in data])
        print(f'I: Smaling smali_{targetdir} folder into {targetdir}.dex')
        utils.call(f'java -jar bin/apktool/smali.jar a --api {port_android_sdk} tmp/{targetdir} -o tmp/{targetdir}.dex')
        with zipfile.ZipFile(frameworkjar, 'a') as frame:
            frame.write(f'tmp/{targetdir}.dex', f'{targetdir}.dex', zipfile.ZIP_DEFLATED)
        for file in os.listdir('BASEROM/images/system/system/framework'):
            if file.startswith('boot-framework'):
                continue
            elif file.endswith('.vdex'):
                try:
                    os.remove(os.path.join('BASEROM/images/system/system/framework', file))
                except:
                    pass
        for file in os.listdir('BASEROM/images/system/system/framework/arm'):
            if file.startswith('boot-framework'):
                continue
            elif file:
                try:
                    os.remove(os.path.join('BASEROM/images/system/system/framework/arm', file))
                except:
                    pass
        for file in os.listdir('BASEROM/images/system/system/framework/arm64'):
            if file.startswith('boot-framework'):
                continue
            elif file:
                try:
                    os.remove(os.path.join('BASEROM/images/system/system/framework/arm64', file))
                except:
                    pass
        for root, dirs, files in os.walk('BASEROM/images/'):
            for dir_ in dirs:
                if os.path.basename(dir_) == 'oat':
                    shutil.rmtree(os.path.join(root, dir_))
        shutil.rmtree('tmp')
    else:
        print('I: Skipping modify framework.jar')
        shutil.rmtree('tmp')
else:
    Yellow('I: Skipping modify framework.jar')
if os.path.isfile('BASEROM/images/system/system/etc/init/hw/init.rc'):
    with open('BASEROM/images/system/system/etc/init/hw/init.rc', 'r', encoding='utf-8') as f:
        data = f.readlines()
    with open('BASEROM/images/system/system/etc/init/hw/init.rc', 'w', encoding='utf-8') as f:
        for i in data:
            if i == 'on boot\n':
                f.write(i)
                f.write('chmod 0731 /data/system/theme\n')
            else:
                f.write(i)
