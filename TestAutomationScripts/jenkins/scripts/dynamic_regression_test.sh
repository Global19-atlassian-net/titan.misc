#!/bin/sh -xe
env
cd TTCNv3

rm -frv regression_test_DYN
cp -frv regression_test regression_test_DYN
cd regression_test_DYN
make distclean

#negative tests turn on:
#sed -i 's|filename_stem := "verdictoper-xml"||' verdictOper/config.cfg

sed -i 's:ERC::' Makefile
sed -i 's:logFiles::' Makefile
sed -i 's:CRTR00015758::' Makefile

find -iname "*.cfg" | while read -r file; do
  if grep -Fq "[LOGGING]" "$file"; then
    sed -i '/\[LOGGING\]/ a\LoggerPlugins := { JUnitLogger := "libjunitlogger" }' "$file"; 
  else
    sed -i '1i[LOGGING]\nLoggerPlugins := { JUnitLogger := "libjunitlogger" }' "$file";
  fi
done

#the few tests where the ttcn3_makefilgen has been used to generate makefiles
#not too elegant, need a proper find and grep to do this, but who knows the consequences?
sed -i 's:$TTCN3_DIR/bin/ttcn3_makefilegen:$TTCN3_DIR/bin/ttcn3_makefilegen -l:g' XML/XmlWorkflow/bin/prj2mk.pl

find cfgFile -iname "Makefile" | while read -r file; do
  sed -i 's:$(TTCN3_DIR)/bin/ttcn3_makefilegen:$(TTCN3_DIR)/bin/ttcn3_makefilegen -l:g' "$file"; 
done

sed -i 's:ttcn3_makefilegen:ttcn3_makefilegen -l :g' "lazyEval/Makefile";
sed -i 's:ttcn3_makefilegen:ttcn3_makefilegen -l :g' "tryCatch/Makefile";
sed -i 's:ttcn3_makefilegen:ttcn3_makefilegen -l :g' "text2ttcn/Makefile";
sed -i 's:TTCN3_LIB = ttcn3-parallel:TTCN3_LIB = ttcn3-parallel-dynamic:g' "logger/emergency_logging/Makefile";

export LD_LIBRARY_PATH=$WORKSPACE/TTCNv3/loggerplugins/JUnitLogger:$LD_LIBRARY_PATH
make prereq DYN=1
make DYN=1
make run DYN=1

find cfgFile/ordered_include/dir_parallel_mode -iname "*.log" | while read -r file; do
mv $file $file.tmp
done
