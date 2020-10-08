#!/bin/bash

## ---VARIABLES---
## $NIGHTLY_DIR comes from Jenkins
HOST=$(hostname -s)
TRTHOME="/home/titanrt"
SSHKEY="$TRTHOME/.ssh/id_rsa_to_hub"
DESTDIR="/proj/ttcn3titan/www/ttcn/root/download/packages/"
MINSIZE=15000000

## ---CLEANUP---
if
  [ -e ttcn3-nightly-linux64-*.tgz ]; then
  rm -f ttcn3-nightly-linux64-*.tgz
fi 

## ---GET DISTRO---
if
  [ $HOST = "tcclab1" ]; then
  DIST="gcc4.3-suse11"
fi

if
  [ $HOST = "tcclab2" ]; then
  DIST="gcc4.6-ubuntu-12.04"
fi

if
  [ $HOST = "tcclab5" ]; then
  DIST="gcc5.4-ubuntu-16.04"
fi

if
  [ $HOST = "tcclab4" ]; then
  DIST="gcc4.8-ubuntu-14.04"
fi


#grep -i suse /etc/*release
#if
#  [ $? = 0 ]; then
#  DIST="gcc4.3-suse-11"
#else
#  DIST="gcc4.6-ubuntu-12.04"
#fi

## ---TEST---
#$NIGHTLY_DIR/demo/MyExample
#if
#  [ $? != 0 ]; then
#  echo "Test failed, abort."
#  exit 1
#fi

## ---CREATE PACKAGE---
tar -cvzf ttcn3-nightly-linux64-$DIST.tgz -C $NIGHTLY_DIR .
TGZSIZE=$(stat -c %s ttcn3-nightly-linux64-$DIST.tgz)
if
  [ $MINSIZE -gt $TGZSIZE ]; then
  echo "Something is missing, abort."
  exit 2
fi  

## ---PUBLISH---
if
  [ ! -e $SSHKEY ]; then
  echo "SSH key missing, abort."
  exit 3
fi
scp -vi $SSHKEY ttcn3-nightly-linux64-$DIST.tgz etccadmi1@hub:$DESTDIR
if
  [ $? = 0 ]; then
  echo "File transfer complete."
  exit 0
else
  echo "File transfer failed."
  exit 4
fi
