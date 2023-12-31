# 删除多余的App
rm -rf BASEROM/images/product/app/MSA
rm -rf BASEROM/images/product/priv-app/MSA
rm -rf BASEROM/images/product/app/mab
rm -rf BASEROM/images/product/priv-app/mab
rm -rf BASEROM/images/product/app/Updater
rm -rf BASEROM/images/product/priv-app/Updater
rm -rf BASEROM/images/product/app/MiuiUpdater
rm -rf BASEROM/images/product/priv-app/MiuiUpdater
rm -rf BASEROM/images/product/app/MIUIUpdater
rm -rf BASEROM/images/product/priv-app/MIUIUpdater
rm -rf BASEROM/images/product/app/MiService
rm -rf BASEROM/images/product/app/MIService
rm -rf BASEROM/images/product/priv-app/MiService
rm -rf BASEROM/images/product/priv-app/MIService
rm -rf BASEROM/images/product/app/*Hybrid*
rm -rf BASEROM/images/product/priv-app/*Hybrid*
rm -rf BASEROM/images/product/etc/auto-install*
rm -rf BASEROM/images/product/app/AnalyticsCore/*
rm -rf BASEROM/images/product/priv-app/AnalyticsCore/*
rm -rf BASEROM/images/product/data-app/*GalleryLockscreen*
mkdir -p app
mv BASEROM/images/product/data-app/*Weather* app/
mv BASEROM/images/product/data-app/*DeskClock* app/
mv BASEROM/images/product/data-app/*Gallery* app/
mv BASEROM/images/product/data-app/*SoundRecorder* app/
mv BASEROM/images/product/data-app/*ScreenRecorder* app/
mv BASEROM/images/product/data-app/*Calculator* app/
mv BASEROM/images/product/data-app/*Calendar* app/
rm -rf BASEROM/images/product/data-app/*
cp -rf app/* BASEROM/images/product/data-app
rm -rf app
rm -rf BASEROM/images/system/verity_key
rm -rf BASEROM/images/vendor/verity_key
rm -rf BASEROM/images/product/verity_key
rm -rf BASEROM/images/system/recovery-from-boot.p
rm -rf BASEROM/images/vendor/recovery-from-boot.p
rm -rf BASEROM/images/product/recovery-from-boot.p
rm -rf BASEROM/images/product/media/theme/miui_mod_icons/com.google.android.apps.nbu*
rm -rf BASEROM/images/product/media/theme/miui_mod_icons/dynamic/com.google.android.apps.nbu*

# build.prop 修改
Yellow "正在修改 build.prop"
buildDate=$(date -u +"%a %b %d %H:%M:%S UTC %Y")
buildUtc=$(date +%s)
for i in $(find BASEROM/images/ -type f -name "build.prop");do
    Yellow "正在处理 ${i}"
    sed -i "s/ro.odm.build.date=.*/ro.odm.build.date=${buildDate}/g" ${i}
    sed -i "s/ro.odm.build.date.utc=.*/ro.odm.build.date.utc=${buildUtc}/g" ${i}
    sed -i "s/ro.vendor.build.date=.*/ro.vendor.build.date=${buildDate}/g" ${i}
    sed -i "s/ro.vendor.build.date.utc=.*/ro.vendor.build.date.utc=${buildUtc}/g" ${i}
    sed -i "s/ro.system.build.date=.*/ro.system.build.date=${buildDate}/g" ${i}
    sed -i "s/ro.system.build.date.utc=.*/ro.system.build.date.utc=${buildUtc}/g" ${i}
    sed -i "s/ro.product.build.date=.*/ro.product.build.date=${buildDate}/g" ${i}
    sed -i "s/ro.product.build.date.utc=.*/ro.product.build.date.utc=${buildUtc}/g" ${i}
    sed -i "s/ro.system_ext.build.date=.*/ro.system_ext.build.date=${buildDate}/g" ${i}
    sed -i "s/ro.system_ext.build.date.utc=.*/ro.system_ext.build.date.utc=${buildUtc}/g" ${i}
    sed -i "s/ro.build.date=.*/ro.build.date=${buildDate}/g" ${i}
    sed -i "s/ro.build.date.utc=.*/ro.build.date.utc=${buildUtc}/g" ${i}
    sed -i "s/ro.odm.build.version.incremental=.*/ro.odm.build.version.incremental=${port_rom_version}/g" ${i}
    sed -i "s/ro.vendor.build.version.incremental=.*/ro.vendor.build.version.incremental=${port_rom_version}/g" ${i}
    sed -i "s/ro.system.build.version.incremental=.*/ro.system.build.version.incremental=${port_rom_version}/g" ${i}
    sed -i "s/ro.product.build.version.incremental=.*/ro.product.build.version.incremental=${port_rom_version}/g" ${i}
    sed -i "s/ro.system_ext.build.version.incremental=.*/ro.system_ext.build.version.incremental=${port_rom_version}/g" ${i}
    sed -i "s/ro.product.device=.*/ro.product.device=${base_rom_code}/g" ${i}
    sed -i "s/ro.product.odm.device=.*/ro.product.odm.device=${base_rom_code}/g" ${i}
    sed -i "s/ro.product.vendor.device=.*/ro.product.vendor.device=${base_rom_code}/g" ${i}
    sed -i "s/ro.product.system.device=.*/ro.product.system.device=${base_rom_code}/g" ${i}
    sed -i "s/ro.product.board=.*/ro.product.board=${base_rom_code}/g" ${i}
    sed -i "s/ro.product.system_ext.device=.*/ro.product.system_ext.device=${base_rom_code}/g" ${i}
    sed -i "s/persist.sys.timezone=.*/persist.sys.timezone=Asia\/Shanghai/g" ${i}
    sed -i "s/ro.product.mod_device=.*/ro.product.mod_device=${base_rom_code}/g" ${i}
done

sed -i '$a\persist.adb.notify=0' BASEROM/images/system/system/build.prop
sed -i '$a\persist.sys.usb.config=mtp,adb' BASEROM/images/system/system/build.prop
sed -i '$a\persist.sys.disable_rescue=true' BASEROM/images/system/system/build.prop
sed -i '$a\persist.miui.extm.enable=0' BASEROM/images/system/system/build.prop

# 屏幕密度修修改
for prop in $(find BASEROM/images/product_bak BASEROM/images/system_bak -type f -name "build.prop");do
    base_rom_density=$(cat $prop |grep "ro.sf.lcd_density" |awk 'NR==1' |cut -d '=' -f 2)
    if [ "${base_rom_density}" != "" ];then
        Green "底包屏幕密度值 ${base_rom_density}"
        break
    fi
done

# 未在底包找到则默认440,如果是其他值可自己修改
[ -z ${base_rom_density} ] && base_rom_density=440

for prop in $(find BASEROM/images/product_bak BASEROM/images/system_bak -type f -name "build.prop");do
    sed -i "s/ro.sf.lcd_density=.*/ro.sf.lcd_density=${base_rom_density}/g" ${prop}
    sed -i "s/persist.miui.density_v2=.*/persist.miui.density_v2=${base_rom_density}/g" ${prop}
done


vendorprop=$(find BASEROM/images/vendor/ -type f -name "build.prop")
odmprop=$(find BASEROM/images/odm/ -type f -name "build.prop" |awk 'NR==1')
if [ "$(cat $vendorprop |grep "sys.haptic" |awk 'NR==1')" != "" ];then
    Yellow "复制 haptic prop 到 odm"
    cat $vendorprop |grep "sys.haptic" >>${odmprop}
fi

# 重新打包镜像
rm -rf BASEROM/images/system_bak*
rm -rf BASEROM/images/product_bak*
rm -rf BASEROM/images/system_ext_bak*
for pname in ${PORT_PARTITION};do
    rm -rf BASEROM/images/${pname}.img
done
echo "${packType}">fstype.txt
superSize=$(bash bin/getSuperSize.sh $deviceCode)
Green 开始打包镜像
for pname in ${SUPERLIST};do
    if [ -d "BASEROM/images/$pname" ];then
        thisSize=$(du -sb BASEROM/images/${pname} |tr -cd 0-9)
        case $pname in
            mi_ext) addSize=4194304 ;;
            odm) addSize=134217728 ;;
            system|vendor|system_ext) addSize=154217728 ;;
            product) addSize=204217728 ;;
            *) addSize=8554432 ;;
        esac
        if [ "$packType" = "ext4" ];then
            Yellow "$pname"为EXT4文件系统多分配大小$addSize
            for fstab in $(find BASEROM/images/${pname}/ -type f -name "fstab.*");do
                sed -i '/overlay/d' $fstab
                sed -i '/system * erofs/d' $fstab
                sed -i '/system_ext * erofs/d' $fstab
                sed -i '/vendor * erofs/d' $fstab
                sed -i '/product * erofs/d' $fstab
            done
            thisSize=$(echo "$thisSize + $addSize" |bc)
            Yellow 以[$packType]文件系统打包[${pname}.img]大小[$thisSize]
            make_ext4fs -J -T $(date +%s) -S BASEROM/config/${pname}_file_contexts -l $thisSize -C BASEROM/config/${pname}_fs_config -L ${pname} -a ${pname} BASEROM/images/${pname}.img BASEROM/images/${pname}
            if [ -f "BASEROM/images/${pname}.img" ];then
                Green "成功以大小 [$thisSize] 打包 [${pname}.img] [${packType}] 文件系统"
                rm -rf BASEROM/images/${pname}
            else
                Error "以 [${packType}] 文件系统打包 [${pname}] 分区失败"
            fi
        else
            Yellow 以[$packType]文件系统打包[${pname}.img]
            mkfs.erofs --mount-point ${pname} --fs-config-file BASEROM/config/${pname}_fs_config --file-contexts BASEROM/config/${pname}_file_contexts BASEROM/images/${pname}.img BASEROM/images/${pname}
            if [ -f "BASEROM/images/${pname}.img" ];then
                Green "成功以 [erofs] 文件系统打包 [${pname}.img]"
                rm -rf BASEROM/images/${pname}
            else
                Error "以 [${packType}] 文件系统打包 [${pname}] 分区失败"
            fi
        fi
        unset fsType
        unset thisSize
    fi
done
rm fstype.txt



# 打包 super.img
Yellow 开始打包Super.img

lpargs="-F --virtual-ab --output BASEROM/images/super.img --metadata-size 65536 --super-name super --metadata-slots 3 --device super:$superSize --group=qti_dynamic_partitions_a:$superSize --group=qti_dynamic_partitions_b:$superSize"

for pname in ${SUPERLIST};do
    if [ -f "BASEROM/images/${pname}.img" ];then
        subsize=$(du -sb BASEROM/images/${pname}.img |tr -cd 0-9)
        Green Super 子分区 [$pname] 大小 [$subsize]
        args="--partition ${pname}_a:none:${subsize}:qti_dynamic_partitions_a --image ${pname}_a=BASEROM/images/${pname}.img --partition ${pname}_b:none:0:qti_dynamic_partitions_b"
        lpargs="$lpargs $args"
        unset subsize
        unset args
    fi
done
lpmake $lpargs
if [ -f "BASEROM/images/super.img" ];then
    Green 成功打包 Super.img
else
    Error 无法打包 Super.img
fi
for pname in ${SUPERLIST};do
    rm -rf BASEROM/images/${pname}.img
done

Yellow "正在压缩 super.img"
zstd --rm BASEROM/images/super.img

# disable vbmeta
for img in $(find BASEROM/images/ -type f -name "vbmeta*.img");do
    vbmeta-disable-verification $img
done


mkdir -p PORT_${deviceCode}_${port_rom_version}/images
mkdir -p PORT_${deviceCode}_${port_rom_version}/META-INF/com/google/android/
cp -rf bin/flash/update-binary PORT_${deviceCode}_${port_rom_version}/META-INF/com/google/android/
cp -rf bin/flash/platform-tools-windows PORT_${deviceCode}_${port_rom_version}/META-INF/
cp -rf bin/flash/flash_update.bat PORT_${deviceCode}_${port_rom_version}/
cp -rf bin/flash/flash_and_format.bat PORT_${deviceCode}_${port_rom_version}/
mv -f BASEROM/images/super.img.zst PORT_${deviceCode}_${port_rom_version}/images/
mv -f BASEROM/images/*.img PORT_${deviceCode}_${port_rom_version}/images/
cp -rf bin/flash/zstd PORT_${deviceCode}_${port_rom_version}/META-INF/

# 生成刷机脚本
Yellow "正在生成刷机脚本"
for fwImg in $(ls PORT_${deviceCode}_${port_rom_version}/images/ |cut -d "." -f 1 |grep -vE "super|cust|preloader");do
    if [ "$(echo $fwImg |grep vbmeta)" != "" ];then
        sed -i "/rem/a META-INF\\\platform-tools-windows\\\fastboot --disable-verity --disable-verification flash "$fwImg"_b images\/"$fwImg".img" PORT_${deviceCode}_${port_rom_version}/flash_update.bat
        sed -i "/rem/a META-INF\\\platform-tools-windows\\\fastboot --disable-verity --disable-verification flash "$fwImg"_a images\/"$fwImg".img" PORT_${deviceCode}_${port_rom_version}/flash_update.bat
        sed -i "/rem/a META-INF\\\platform-tools-windows\\\fastboot --disable-verity --disable-verification flash "$fwImg"_b images\/"$fwImg".img" PORT_${deviceCode}_${port_rom_version}/flash_and_format.bat
        sed -i "/rem/a META-INF\\\platform-tools-windows\\\fastboot --disable-verity --disable-verification flash "$fwImg"_a images\/"$fwImg".img" PORT_${deviceCode}_${port_rom_version}/flash_and_format.bat
        sed -i "/#firmware/a package_extract_file \"images/"$fwImg".img\" \"/dev/block/bootdevice/by-name/"$fwImg"_b\"" PORT_${deviceCode}_${port_rom_version}/META-INF/com/google/android/update-binary
        sed -i "/#firmware/a package_extract_file \"images/"$fwImg".img\" \"/dev/block/bootdevice/by-name/"$fwImg"_a\"" PORT_${deviceCode}_${port_rom_version}/META-INF/com/google/android/update-binary
    else
        sed -i "/rem/a META-INF\\\platform-tools-windows\\\fastboot flash "$fwImg"_b images\/"$fwImg".img" PORT_${deviceCode}_${port_rom_version}/flash_update.bat
        sed -i "/rem/a META-INF\\\platform-tools-windows\\\fastboot flash "$fwImg"_a images\/"$fwImg".img" PORT_${deviceCode}_${port_rom_version}/flash_update.bat
        sed -i "/rem/a META-INF\\\platform-tools-windows\\\fastboot flash "$fwImg"_b images\/"$fwImg".img" PORT_${deviceCode}_${port_rom_version}/flash_and_format.bat
        sed -i "/rem/a META-INF\\\platform-tools-windows\\\fastboot flash "$fwImg"_a images\/"$fwImg".img" PORT_${deviceCode}_${port_rom_version}/flash_and_format.bat
        sed -i "/#firmware/a package_extract_file \"images/"$fwImg".img\" \"/dev/block/bootdevice/by-name/"$fwImg"_b\"" PORT_${deviceCode}_${port_rom_version}/META-INF/com/google/android/update-binary
        sed -i "/#firmware/a package_extract_file \"images/"$fwImg".img\" \"/dev/block/bootdevice/by-name/"$fwImg"_a\"" PORT_${deviceCode}_${port_rom_version}/META-INF/com/google/android/update-binary
    fi
done

sed -i "s/portversion/${port_rom_version}/g" PORT_${deviceCode}_${port_rom_version}/META-INF/com/google/android/update-binary
sed -i "s/baseversion/${base_rom_version}/g" PORT_${deviceCode}_${port_rom_version}/META-INF/com/google/android/update-binary
sed -i "s/andVersion/${port_android_version}/g" PORT_${deviceCode}_${port_rom_version}/META-INF/com/google/android/update-binary
sed -i "s/deviceCode/${base_rom_code}/g" PORT_${deviceCode}_${port_rom_version}/META-INF/com/google/android/update-binary

busybox unix2dosPORT_${deviceCode}_${port_rom_version}/flash_update.bat
busybox unix2dos PORT_${deviceCode}_${port_rom_version}/flash_and_format.bat

find PORT_${deviceCode}_${port_rom_version}/ |xargs touch

cd PORT_${deviceCode}_${port_rom_version}/
zip -r PORT_${deviceCode}_${port_rom_version}.zip ./*
mv PORT_${deviceCode}_${port_rom_version}.zip ../
cd ../
hash=$(md5sum PORT_${deviceCode}_${port_rom_version}.zip |head -c 10)
mv PORT_${deviceCode}_${port_rom_version}.zip PORT_${deviceCode}_${port_rom_version}_${hash}_${port_android_version}.zip
Green "移植完毕"
Green "输出包为 $(pwd)/PORT_${deviceCode}_${port_rom_version}_${hash}_${port_android_version}.zip"