#!/bin/sh -xe
env
cd TTCNv3
if [ ! -f function_test/Semantic_Analyser/perl ] ; then ln -s $PERL_PATH/perl function_test/Semantic_Analyser/perl; fi;
if [ ! -f function_test/Config_Parser/perl ] ; then ln -s $PERL_PATH/perl function_test/Config_Parser/perl; fi;

#make -C function_test -j${NUM_PROCESSORS} -- logs will be mixed!!!
make -C function_test
