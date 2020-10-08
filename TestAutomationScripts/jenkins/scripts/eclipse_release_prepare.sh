#!/bin/bash
TMPROOTDIR="/home/titanrt/eclipse_automatic_build/tmp_update_sites"
TMPSITEDIR="Testing_update_site"
WWWROOTDIR="/proj/TTCN/www/ttcn/root/download/"
WWWSITEDIR="testing_update_site"
STAMP=`date +%F`
 
if [ "$(ls -A $TMPROOTDIR/$TMPSITEDIR)" ]; then
  tar -cvjf $TMPROOTDIR/$TMPSITEDIR-$STAMP.tar.bz2 -C $TMPROOTDIR/$TMPSITEDIR .
  rm -rf $TMPROOTDIR/$TMPSITEDIR/*
elif [ "$(ls -A $WWWROOTDIR/$WWWSITEDIR)" ]; then
  tar -cvjf $WWWROOTDIR/$WWWSITEDIR-$STAMP.tar.bz2 -C $WWWROOTDIR/$WWWSITEDIR .
  rm -rf $WWWROOTDIR/$WWWSITEDIR/*  
else
  echo "Empty folders, let's build."
fi

