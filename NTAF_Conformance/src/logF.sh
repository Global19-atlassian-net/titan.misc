#!/bin/sh

##############################################################################/
## Copyright (c) 2000-2021 Ericsson Telecom AB
## All rights reserved. This program and the accompanying materials
## are made available under the terms of the Eclipse Public License v1.0
## which accompanies this distribution, and is available at
## http://www.eclipse.org/legal/epl-v10.html
##
##
## Contributors:
##  Elemer Lelik - initial implementation
##  Endre Kulcsar
##  Eszter Susanszky
##
##  File:               logF.sh
##  Description:        NTAF Conformance Test Suite 
##  Rev:                 
##  Prodnr:              
##  Updated:            2013-09-10
##  Contact:            http://ttcn.ericsson.se
##
##############################################################################/

##############################################################################/
##  Module:  
##
##  Purpose: 
##     
##
##  Module Parameters:
##      -
##
##  Module depends on:
##    -
##
##############################################################################


rm -f NTAF_exec_message.log
ttcn3_logmerge -o NTAF_exec.merged.log NTAF_exec.*.log 
cat NTAF_exec.merged.log | grep '>>>---->>>'  >> NTAF_exec_message.f.log
rm -f NTAF_exec.merged.log

for logfile in `ls *.log`; do
#echo $logfile
ttcn3_logformat $logfile > $logfile.f.log
done

DATE=$(date +"%y%m%d")
TIME=$(date +"%H%M%S")
#echo $DATE$TIME

tar cvzf formatted_lox$DATE$TIME.tgz *.f.log
mv formatted_lox$DATE$TIME.tgz ../src/
cat *mtc.log.f.log | grep 'Verdict: '

sed 's/\\n/\n/g' NTAF_exec_message.f.log > NTAF_exec_message.log
rm -f *.f.log

