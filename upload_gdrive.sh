#!/bin/bash
echo Gdrive start

PREFIX="lineage-14.1-"
POSTFIX="-UNOFFICIAL-gemini"
DATE=`date +%Y%m%d`

PATH="android/system/out/target/product/gemini/"
GDRIVE_PARENT="0B1UDBYCQNGW7SV9zNGxkYjFHYVk"


BUILD=$PREFIX$DATE$POSTFIX".zip"
MD5=$BUILD".md5sum"

echo "Datum: " $DATE
echo "Build: " $BUILD
echo "MD5:   " $MD5
echo "Target:" $PATH

./gdrive upload -p $GDRIVE_PARENT $PATH$BUILD
./gdrive upload -p $GDRIVE_PARENT $PATH$MD5

echo Gdrive ende
