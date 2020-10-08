#!/bin/sh -xe
env
cd TTCNv3

make -C regression_test distclean
make -C regression_test prereq
make -C regression_test report
