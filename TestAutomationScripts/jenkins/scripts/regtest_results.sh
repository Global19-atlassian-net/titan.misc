#!/bin/bash

# Define static variables
#WORKSPACE="/local/titanrt/jenkins/workspace/Nightly_GIT_Titan_build/slaves/titanrt_tcclab5"
WORKDIR="$WORKSPACE/TTCNv3/regression_test"

# Define dynamic variables
DEFINE_VARIABLES() {
  RT=$1
  TXT="$WORKDIR/report_$RT.txt"
  PASSED_TXT="$WORKDIR/passed_$RT.txt"
  FAILED_TXT="$WORKDIR/failed_$RT.txt"
  INCONC_TXT="$WORKDIR/inconc_$RT.txt"
  SUM_XML="$WORKDIR/regtest_sum_report_$RT.xml"
}


# Make a clean environment in workdir
function CLEANUP {
  rm -f "$PASSED_TXT"
  rm -f "$FAILED_TXT"
  rm -f "$INCONC_TXT"
  rm -f "$SUM_XML"
}


# Collect test cases and verdicts and filter out false positive cases
function COLLECT_VERDICT {
  while read -r testcase
  do
    if [[ $testcase == *"Verdict: pass"* ]]; then
      if [[ $testcase == *Fail* ]]; then
        echo "$testcase" | awk -F "Test case" '{split($2, a, " "); print a[1]}' >> $FAILED_TXT
      else echo "$testcase" | awk -F "Test case" '{split($2, a, " "); print a[1]}' >> $PASSED_TXT
      fi
    elif [[ $testcase == *"Verdict: fail"* ]]; then
      if [[ $testcase == *Fail* ]]; then
        echo "$testcase" | awk -F "Test case" '{split($2, a, " "); print a[1]}' >> $PASSED_TXT
      else
        echo "$testcase" | awk -F "Test case" '{split($2, a, " "); print a[1]}' $FAILED_TXT
      fi
    elif [[ $testcase == *"Verdict: inconc"* ]]; then
      if [[ $testcase == *Inconc* ]]; then
        echo "$testcase" | awk -F "Test case" '{split($2, a, " "); print a[1]}' >> $PASSED_TXT
      else
        echo "$testcase" | awk -F "Test case" '{split($2, a, " "); print a[1]}' >> $INCONC_TXT
      fi
    fi
  done <<< "`grep "Test case" $TXT | grep "Verdict:"`"
}


# Make a count for each verdicts
function COUNT_CASES {
  if [ -f $PASSED_TXT ]; then
    PASS=$(cat $PASSED_TXT | wc -l)
  else
    PASS="0"
  fi
  if [ -f $FAILED_TXT ]; then
    FAILED=$(cat $FAILED_TXT | wc -l)
  else FAILED="0"
  fi
  if [ -f $INCONC_TXT ]; then
    INCONC=$(cat $INCONC_TXT | wc -l)
  else INCONC="0"
  fi
}


# Create summary .xml
function CREATE_XML {
  echo '<section name="'$HOSTNAME' regression test '$RT' results">' > $SUM_XML
  echo '  <table>' >> $SUM_XML
  echo '    <tr>' >> $SUM_XML
  echo '      <td value="Passed" bgcolor="green" fontcolor="black" fontattribute="bold" align="center" width="300"/>' >> $SUM_XML
  echo '      <td value="'$PASS'" bgcolor="white" fontcolor="black" fontattribute="normal" align="center" width="300"/>' >> $SUM_XML
  echo '    </tr>' >> $SUM_XML
  echo '    <tr>' >> $SUM_XML
  echo '      <td value="Failed" bgcolor="red" fontcolor="black" fontattribute="bold" align="center" width="300"/>' >> $SUM_XML
  echo '      <td value="'$FAILED'" bgcolor="white" fontcolor="black" fontattribute="normal" align="center" width="300"/>' >> $SUM_XML
  echo '    </tr>' >> $SUM_XML
  echo '    <tr>' >> $SUM_XML
  echo '      <td value="Inconclusive" bgcolor="yellow" fontcolor="black" fontattribute="bold" align="center" width="300"/>' >> $SUM_XML
  echo '      <td value="'$INCONC'" bgcolor="white" fontcolor="black" fontattribute="normal" align="center" width="300"/>' >> $SUM_XML
  echo '    </tr>' >> $SUM_XML
  echo '  </table>' >> $SUM_XML
  echo '  <accordion name="Passed tests">' >> $SUM_XML
  echo '    <table>' >> $SUM_XML
  if [ -f $PASSED_TXT ]; then
    while read passed_case
    do
       echo '      <tr>' >> $SUM_XML
       echo '        <td value="'$passed_case'" bgcolor="green" fontcolor="black" fontattribute="bold" align="center" width="300"/>' >> $SUM_XML
       echo '      </tr>' >> $SUM_XML
    done <$PASSED_TXT
  fi
  echo '    </table>' >> $SUM_XML
  echo '  </accordion>' >> $SUM_XML
  echo '  <accordion name="Failed tests">' >> $SUM_XML
  echo '    <table>' >> $SUM_XML
  if [ -f $FAILED_TXT ]; then
    while read failed_case
    do
       echo '      <tr>' >> $SUM_XML   
       echo '        <td value="'$failed_case'" bgcolor="red" fontcolor="black" fontattribute="bold" align="center" width="300"/>' >> $SUM_XML
       echo '      </tr>' >> $SUM_XML
    done <$FAILED_TXT
  fi
  echo '    </table>' >> $SUM_XML
  echo '  </accordion>' >> $SUM_XML
  echo '  <accordion name="Inconclusive tests">' >> $SUM_XML
  echo '  <table>' >> $SUM_XML
  if [ -f $INCONC_TXT ]; then
    while read inconc_case
    do
      echo '      <tr>' >> $SUM_XML
      echo '        <td value="'$inconc_case'" bgcolor="yellow" fontcolor="black" fontattribute="bold" align="center" width="300"/>' >> $SUM_XML
      echo '      </tr>' >> $SUM_XML
    done <$INCONC_TXT
  fi
  echo '    </table>' >> $SUM_XML
  echo '  </accordion>' >> $SUM_XML
  echo '</section>' >> $SUM_XML
}

# Results for the RT1 tests
DEFINE_VARIABLES RT1
CLEANUP
COLLECT_VERDICT
COUNT_CASES
CREATE_XML

 # Results for the RT2 tests
DEFINE_VARIABLES RT2
CLEANUP
COLLECT_VERDICT
COUNT_CASES
CREATE_XML
