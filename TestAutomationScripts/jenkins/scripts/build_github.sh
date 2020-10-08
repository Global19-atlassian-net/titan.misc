#!/bin/sh -xe
alias make /usr/bin/make
pseudo_mod="no"

while [ "$1" != "" ]; do
    case $1 in
        -p | --pseudo )
	                    pseudo_mod="yes"
                        ;;
	esac
    shift
done

cd TTCNv3
#make prereq
/usr/bin/make dep
/usr/bin/make -j${NUM_PROCESSORS} 
#make -j${NUM_PROCESSORS} -C Install

if [ "$pseudo_mod" != "yes" ]
then
	perl -pi -e 's|TTCN3_DIR := (.*)|TTCN3_DIR := \$\{WORKSPACE\}/TTCNv3/Install|' Makefile.cfg
	
	#for Solaris (instead of error code 1 from= "chmod: WARNING: can't access" because of the broken symlinks in help/docs)
	cd usrguide
	touch apiguide.pdf  installationguide.pdf referenceguide.pdf  releasenotes.pdf  userguide.pdf userguide_mctr_gui.pdf
	cd ..
	/usr/bin/make install GEN_PDF=yes
	
else
	/usr/bin/make -j${NUM_PROCESSORS} -C Install
fi
