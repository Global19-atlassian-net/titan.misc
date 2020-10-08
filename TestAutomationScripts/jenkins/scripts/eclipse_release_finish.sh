#!/bin/bash
TMPROOTDIR="/home/titanrt/eclipse_automatic_build/tmp_update_sites"
TMPSITEDIR="Testing_update_site"
WWWROOTDIR="/proj/TTCN/www/ttcn/root/download"
WWWSITEDIR="testing_update_site"
STAMP=`date +%F`

pushd $TMPROOTDIR/$TMPSITEDIR
zip -r $TMPROOTDIR/TITAN_Designer_and_Executor_plugin-$VERSION.zip *
popd

if [ -f $TMPROOTDIR/$TMPSITEDIR-$STAMP.tar.bz2 ]; then
  tar -xvjf $TMPROOTDIR/$TMPSITEDIR-$STAMP.tar.bz2 -C $TMPROOTDIR/$TMPSITEDIR 
  if [ $? = 0 ]; then
    rm -f $TMPROOTDIR/$TMPSITEDIR-$STAMP.tar.bz2
  fi
elif [ -f $WWWROOTDIR/$WWWSITEDIR-$STAMP.tar.bz2 ]; then
  tar -xvjf $WWWROOTDIR/$WWWSITEDIR-$STAMP.tar.bz2 -C $WWWROOTDIR/$WWWSITEDIR 
  if [ $? = 0 ]; then
    rm -f $WWWROOTDIR/$WWWSITEDIR-$STAMP.tar.bz2  
  fi
else
  echo "Missing files, something is wrong."
fi

