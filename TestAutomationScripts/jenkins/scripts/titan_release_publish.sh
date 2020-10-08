#!/bin/bash

## variables, VERSION_STRING comes from Jenkins
export TITAN_DOWNLOAD="/proj/ttcn3titan/www/ttcn/root/download"

if [ "$OPENSOURCE" = "true" ]; then
  export PACKAGE_DIR="/home/titanrt/jenkins/workspace/titan_release/packages_opensource"
  export TARGET_DIR=$TITAN_DOWNLOAD/packages/opensource/$VERSION_STRING
else
  export PACKAGE_DIR="/home/titanrt/jenkins/workspace/titan_release/packages_ericsson"
  export TARGET_DIR=$TITAN_DOWNLOAD/packages/$VERSION_STRING
fi

mkdir -p $TARGET_DIR

scp $PACKAGE_DIR/* $TARGET_DIR

if
  [ $? = 0 ]; then 
  echo "File transfer complete."
  exit 0
else
  echo "File transfer failed."
  exit 1
fi

