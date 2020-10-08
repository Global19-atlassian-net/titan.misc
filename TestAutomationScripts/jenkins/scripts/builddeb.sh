#!/bin/bash

## ---PARAMETER CHECK---
if [ -z "$1" ]; then
    echo "Usage: builddeb.sh [URL]"
    exit 1
fi

## ---VARIABLES---
export LANG=en_EN.UTF8
PATH=/sbin:/bin:/usr/sbin:/usr/bin
TGZ=$(echo $1 | awk -F/ '{print $(NF)}')
FILENAME=$(echo $TGZ | awk -F.tgz '{print $(NF-1)}')
PACKAGENAME=$( echo $FILENAME | awk -F- '{print $1 "-" $2}')
VERSION="4.1.pl0-0ericsson3"
MAIN_VERSION="4"
RELEASE_VERSION="R1A"
FULL_VERSION="CRL 113 200/4/R1A"
CONTROL_FILE="$FILENAME/DEBIAN/control"
#ARCH=$(echo $FILENAME | awk -F- '{print $3}')
#TRTHOME="/home/titanrt"
#SSHKEY="$TRTHOME/.ssh/id_rsa_to_hub"
#DESTDIR="/proj/ttcn3titan/www/ttcn/root/download/packages"

## ---GET THE .TGZ---
if [ ! -d $FILENAME ]; then
    mkdir -p $FILENAME/opt/titan/$MAIN_VERSION/$RELEASE_VERSION/
fi
wget --directory-prefix=$FILENAME $1
tar -xvzf $FILENAME/$TGZ -C $FILENAME/opt/titan/$MAIN_VERSION/$RELEASE_VERSION

## ---CREATE THE CONTROL FILE---
if [ ! -d $FILENAME/DEBIAN ]; then
    mkdir -p $FILENAME/DEBIAN
fi

echo "Package: $PACKAGENAME" > $CONTROL_FILE
echo "Version: $VERSION" >> $CONTROL_FILE
echo "Priority: optional" >> $CONTROL_FILE
echo "Section: utils" >> $CONTROL_FILE
echo "Architecture: amd64" >> $CONTROL_FILE
echo "Depends: titan-essentials (>= 1.1-0ericsson1), libc6" >> $CONTROL_FILE
echo "Maintainer: Test Compentence Center ETH <ttcn3@ex1.eemea.ericsson.se>" >> $CONTROL_FILE
echo "Description: TITAN TTCN-3 toolset version $FULL_VERSION" >> $CONTROL_FILE
echo "Conflicts: $PACKAGENAME" >> $CONTROL_FILE

dpkg-deb --build $FILENAME
