#!/bin/sh -xe
env
cd TTCNv3/usrguide
chmod a+x pdfgen.sh
./pdfgen.sh
cd ..
rm -rf ${WORKSPACE}/RELEASE
mkdir -p ${WORKSPACE}/RELEASE
perl -pi -e 's|TTCN3_DIR := (.*)|TTCN3_DIR := \$\{WORKSPACE\}/RELEASE|' Makefile.cfg
make install TTCN3_DIR=${WORKSPACE}/RELEASE GEN_PDF=yes
cd ${WORKSPACE}/RELEASE
tar -cvzf ${BUILD_ID}_`uname -n` *
mv ${BUILD_ID}_`uname -n` ../${BUILD_ID}_`uname -n`.tgz
