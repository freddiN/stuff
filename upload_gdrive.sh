#!/bin/bash
echo Gdrive start

PREFIX="cm-13.0-"
POSTFIX="-UNOFFICIAL-gemini"
DATE=`date +%Y%m%d`

PATH="android/system/out/target/product/gemini/"
GDRIVE_PARENT="0B1UDBYCQNGW7SV9zNGxkYjFHYVk"


BUILT=$PREFIX$DATE$POSTFIX".zip"
MD5=$BUILT".md5sum"

echo "Datum: " $DATE
echo "Built: " $BUILT
echo "MD5:   " $MD5
echo "Target:" $PATH

./gdrive upload -p $GDRIVE_PARENT $PATH$BUILT
./gdrive upload -p $GDRIVE_PARENT $PATH$MD5

echo Gdrive ende
