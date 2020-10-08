#!/bin/bash

if [ "$OPENSOURCE" = "true" ]; then
  export PACKAGE_DIR="/home/titanrt/jenkins/workspace/titan_release/packages_opensource"
else
  export PACKAGE_DIR="/home/titanrt/jenkins/workspace/titan_release/packages_ericsson"
fi

cd $PACKAGE_DIR

for i in $( ls | grep [A-Z] ) 
  do mv -i $i `echo $i | tr 'A-Z' 'a-z'`
done

for PACKAGENAME in `ls -1 ttcn3*`
  do sha512sum $PACKAGENAME > $PACKAGENAME.sha512
done

