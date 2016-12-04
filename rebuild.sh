#!/bin/bash

cd android/system/

#echo make clean
#make clean
#rm -rf ./out/target/product

echo repo sync
repo sync -j8

echo envsetup.sh
source build/envsetup.sh

echo breakfast
breakfast gemini

echo ccache
export USE_CCACHE=1
#prebuilts/misc/linux-x86/ccache/ccache -M 50G

croot

#export TARGET_PREBUILT_KERNEL=/home/freddi/kernel/zImage

echo brunch
brunch gemini

rm out/target/product/gemini/cm_gemini-ota-*.zip
