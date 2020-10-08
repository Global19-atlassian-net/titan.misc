#!/bin/bash -xe

### VARIABLES, GIT_DIR is not doubled anymore
#RELEASE_SCRIPT="/local/titanrt/jenkins/scripts/titan_release.sh"
GIT_DIR="${WORKSPACE}/git"
#GIT_DIR_OPENSOURCE=${GIT_DIR}
###


### GET CODE
if [ ! -d $GIT_DIR/titan ]; then
    mkdir -p $GIT_DIR
    cd $GIT_DIR
    git clone -v ssh://git@github.com/eclipse/titan.core titan
else
    cd $GIT_DIR/titan
    git clean -fdx
    git reset --hard
    git pull -r
fi

### CREATE WORKDIR (VARIABLE FROM THE JENKINS JOB)
if [ ! -d $WORKDIR ]; then
  mkdir -p $WORKDIR
fi
###

cd $WORKDIR
#rm -rfv *
#cp -aRv $GIT_DIR/titan .
#not verbose:
rm -rf *
cp -aR $GIT_DIR/titan .
cd titan
pwd
git reset --hard $GIT_TAG

if [ "$OPENSOURCE" = "true" ]; then
  sed -i 's/"LICENSING := yes"/"LICENSING := no"/' $RELEASE_SCRIPT
  sed -i 's/"USAGE_STATS := yes"/"USAGE_STATS := no"/'  $RELEASE_SCRIPT
  sed -i 's:/packages_ericsson:/packages_opensource:' $RELEASE_SCRIPT
else
  rm -f MakefileFOSS.cfg
  sed -i 's/"LICENSING := no"/"LICENSING := yes"/' $RELEASE_SCRIPT
  sed -i 's/"USAGE_STATS := no"/"USAGE_STATS := yes"/' $RELEASE_SCRIPT
  sed -i 's:/packages_opensource:/packages_ericsson:' $RELEASE_SCRIPT
fi
###