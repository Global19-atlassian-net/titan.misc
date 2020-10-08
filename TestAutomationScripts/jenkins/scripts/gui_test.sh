#!/usr/bin/sh -x
#-xe
# This thest shall be run on machine esekilxxen1843, under linux
# 1.It starts a jubula autagent
# 2.It starts an eclipse (with cmd autrun)
# 3 it starts a jubula test (with cmd testexec)
#workspace:

#export ECLIPSE_DIR=${WORKSPACE}/eclipse-SDK-4.2-linux-gtk-x86_64
export ECLIPSE_DIR="$HOME/eclipse/eclipse"
JUBULA_WP="$HOME/.jubula"
JUBULA_DIR="$HOME/jubula"
export AUT_WS="$HOME/gui_test/workspace_AUT"
SCRIPT_DIR="$HOME/jenkins/scripts"

if [ -z "${WORKSPACE}" ]
then
  export WORKSPACE="$HOME/gui_test"
fi

echo "Display: $DISPLAY"
echo ${SHELL}
#Xvfb +extension RANDR &
Xvfb :998 &  #-fp /usr/share/fonts/misc  &
XVFB_PID=$!
export DISPLAY="127.0.0.1:998.0"
echo "Display: $DISPLAY"

#pushd .

#WORKSPACE=`pwd`
echo "Workspace: $WORKSPACE"
#===== Preparation: ========
cd "$WORKSPACE"
mkdir -p testresults
mkdir -p testdata
echo ">>>Jubula rc files will be copied"

# copy jubula interface plugin:
cp -f  ${JUBULA_DIR}/development/org.eclipse.jubula.rc.*.jar ${ECLIPSE_DIR}/plugins/

# start jubula interface plugin:
sed -i 's/\(osgi\.bundles=.*\)/\1\,org\.eclipse\.jubula\.rc\.rcp@start/g' ${ECLIPSE_DIR}/configuration/config.ini
sed -i 's/\,org\.eclipse\.jubula\.rc\.rcp@start\,org\.eclipse\.jubula\.rc\.rcp@start/\,org\.eclipse\.jubula\.rc\.rcp@start/g' ${ECLIPSE_DIR}/configuration/config.ini

# Switch off worksace selection dialog:
#if [ -f "${ECLIPSE_DIR}/configuration/.settings/org.eclipse.ui.ide.prefs" ]; then
#  sed -i 's/SHOW_WORKSPACE_SELECTION_DIALOG=true/SHOW_WORKSPACE_SELECTION_DIALOG=false/g'  "${ECLIPSE_DIR}/configuration/.settings/org.eclipse.ui.ide.prefs"
#fi

#===========================================
# Start and stop AUT without testing purpose
#"${ECLIPSE_DIR}/eclipse" -data "$AUT_WS" -clean &
#AUTRUN_PID=$!
#sleep 20
#===========================

cd  ${JUBULA_DIR}/server/
echo ">>>Autagent starts"
date
./autagent -p 60000 -v &
AUTAGENT_PID=$!
sleep 30
echo ">>>>Autrun started"
./autrun -w "${ECLIPSE_DIR}" -i "Config_EclipseDesignerTest_jubula" -rcp -k en_US -e "${SCRIPT_DIR}/start_eclipse_with_ws.sh" &
AUTRUN_PID=$!

sleep 90

cd ${JUBULA_DIR}/jubula
echo ">>>Testexec starts"
./testexec -project "TitanDesignerTestPrototype2" -version "1.3" -testjob "TitanDesignerTestJob_withexit" -server "127.0.0.1" -port 60000 -autid "Config_EclipseDesignerTest_jubula" -datadir "$WORKSPACE/testdata" -resultdir $WORKSPACE/testresults  -data "${JUBULA_WP}" -language "en_US" -dbscheme "Default Embedded (H2)" -dbuser sa -dbpw ""
echo ">>>Testexec finished"
`${JUBULA_DIR}/server/stopautagent`
#popd  

sleep 20
#Cleanup
#kill "$AUTAGENT_PID"
#kill "$AUTRUN_PID"
kill -9 $XVFB_PID
date
echo "Bye"
