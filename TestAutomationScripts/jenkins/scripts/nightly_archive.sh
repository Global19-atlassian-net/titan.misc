#!/bin/bash

DAILYDIR=/proj/ttcn3titan/Releases/TTCNv3_daily
DAILYPACKAGE=ttcn3-nightly-linux64-gcc4.3-suse11.tgz
YESTERDAY=`date --date='yesterday' +%Y-%m-%d` 

cd /proj/ttcn3titan/www/ttcn/root/download/packages
tar -xvzf $DAILYPACKAGE -C $DAILYDIR
FILES=`ls ttcn3-nightly-linux64*`
for FILE in ${FILES}
{
	cp ${FILE} ${YESTERDAY}-$FILE
}

find . -name "*ttcn3-nightly-linux64*" -mtime +7 -exec rm -f {} \;

