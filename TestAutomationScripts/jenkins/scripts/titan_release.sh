#!/bin/bash -xe

### VARIABLES
if [ "$OPENSOURCE" = "true" ]; then
  export PACKAGE_SUFFIX="_foss"
else
  export PACKAGE_SUFFIX=""
fi
echo ${PACKAGE_SUFFIX}
#export PACKAGE_SUFFIX
export HOSTNAME=`hostname -s`
if [ $WORKDIR != "" ]; then
 export WORKDIR
else
 export WORKDIR=/home/titanrt/jenkins/workspace/titan_release/$HOSTNAME
fi
#export WORKDIR=/home/titanrt/jenkins/workspace/titan_release/$HOSTNAME
export TTCN3_DIR=$WORKDIR/titan/Install
export PACKAGE_DIR=/home/titanrt/jenkins/workspace/titan_release/packages_ericsson
export DOCDIR=/home/titanrt/jenkins/workspace/titan_release/docs
#export LICENSEDIR=/home/titanrt/jenkins/workspace/titan_release/license
ARCH=`uname -m`
if [ "$ARCH" = "x86_64" ]; then
  export ARCH="64"
else
  export ARCH="32"
fi

if [ "$CLANG" != "" ]; then
    export GCCVER="clang3.8"
else
    export GCCVER="gcc`g++ -dumpversion`"
fi
#export PKG_VER=`echo $GIT_TAG | sed -e 's!-!.!g' | sed -e 's!^v!!g'`
#export ARCHNAME=`cat /etc/profile.d/titan_comp.sh | grep -i archname | cut -d "\"" -f2` #obsolete
ARCHNAME=`cat /etc/*-release | grep -i PRETTY_NAME | cut -d "\"" -f2`
export ARCHNAME=${ARCHNAME// /_}  #replace spaces for _
export PKGNAME="ttcn3-${PL_VERSION}-linux${ARCH}-${GCCVER}-${ARCHNAME}${PACKAGE_SUFFIX}.tgz"
#export PKGNAME="ttcn3-${PL_VERSION}-linux${ARCH}-${GCCVER}.tgz"
#if [ $ARCH = "32" ]; then
#  export JAVA_HOME=/home/titanrt/jenkins/jdk/jdk32
#else 
#  export JAVA_HOME=/home/titanrt/jenkins/jdk/jdk64
#fi
#export JAVA_BINDIR=$JAVA_HOME/bin
export PATH=$JAVA_BINDIR:$TTCN3_DIR/bin:$PATH
export LD_LIBRARY_PATH=$JAVA_HOME/lib:$TTCN3_DIR/lib:/usr/lib:$LD_LIBRARY_PATH
#export READLINE_DIR=/mnt/TTCN/Tools/readline-5.2
export OPENSSL_DIR=/usr

### BUILD AND INSTALL TITAN
cd $WORKDIR/titan
#These lines will be modified by titan_release_prepare.sh
#These values overwrite any earlier values:
touch Makefile.personal
echo "LICENSING := yes" >> Makefile.personal
echo "USAGE_STATS := yes" >> Makefile.personal
echo "GEN_PDF := no" >> Makefile.personal
echo "TTCN3_DIR := $TTCN3_DIR" >> Makefile.personal
echo "COMPILERFLAGS += -Wall -I$JAVA_HOME/include -I$JAVA_HOME/include/linux" >> Makefile.personal
echo "JDKDIR := $JDKDIR" >> Makefile.personal
if [ "$CLANG" != "" ]; then
    echo "OPENSSL_DIR := /usr " >> Makefile.personal
    echo "XMLDIR := /usr" >> Makefile.personal
    echo "JNI := no" >> Makefile.personal
    echo "GEN_PDF := no" >> Makefile.personal
    echo "CXX := clang++-3.8" >> Makefile.personal
    echo "CC := clang-3.8" >> Makefile.personal
fi

make
make install
if [ ! -d $TTCN3_DIR/doc ]; then
  mkdir -p $TTCN3_DIR/doc
fi
cp $DOCDIR/* $TTCN3_DIR/doc/

#cp $LICENSEDIR/* $TTCN3_DIR/

##create the archive file
if [ ! -d $PACKAGE_DIR ]; then
mkdir -p $PACKAGE_DIR
fi
cd $TTCN3_DIR
tar -cvzf $PACKAGE_DIR/$PKGNAME *




