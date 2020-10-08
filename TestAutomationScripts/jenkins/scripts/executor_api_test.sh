#!/bin/sh -xe

cd $WORKSPACE/TTCNv3/Install/demo
../bin/makefilegen -fg *.ttcn PCOType.hh PCOType.cc
make clean
make
perl -i -p -e 's/(^[^\S\n]*private static Severity sLogLevel = Severity.)[A-Z]+;/\1TRACE;/g' $WORKSPACE/TTCNv3/titan_executor_api/TITAN_Executor_API/src/org/eclipse/titan/executorapi/util/Log.java
cd $WORKSPACE/TTCNv3/titan_executor_api/TITAN_Executor_API_test
ant TITAN_Executor_API_test

