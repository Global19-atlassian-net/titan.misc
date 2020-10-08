#!/bin/bash -xe

### VARIABLES
RELEASE_SCRIPT="/home/titanrt/jenkins/scripts/titan_release.sh"
GIT_DIR="/home/titanrt/jenkins/workspace/titan_release/git"
GIT_DIR_OPENSOURCE="/home/titanrt/jenkins/workspace/titan_release/git_opensource"
###

### CREATE WORKDIR (VARIABLE FROM THE JENKINS JOB)
if [ ! -d $WORKDIR ]; then
  mkdir -p $WORKDIR
fi
###

### NEED TO BE FIXED!!!
#rm -rf $GIT_DIR_OPENSOURCE/titan
#rm -rf $GIT_DIR/titan


### GET CODE
if [ "$OPENSOURCE" = "true" ]; then
  if [ ! -d $GIT_DIR_OPENSOURCE/titan ]; then
    mkdir -p $GIT_DIR_OPENSOURCE
    cd $GIT_DIR_OPENSOURCE
    git clone -v ssh://git@github.com/eclipse/titan.core titan
  else
    cd $GIT_DIR_OPENSOURCE/titan
    git clean -fdx
    git reset --hard
    git pull -r
  fi
  cd $WORKDIR
  #rm -rfv *
  #not verbose:
  rm -rf *
  #cp -aRv $GIT_DIR_OPENSOURCE/titan .
  #not verbose:
  cp -aR $GIT_DIR_OPENSOURCE/titan .
  cd titan
  pwd
  git reset --hard $GIT_TAG
  sed -i 's/"LICENSING := yes"/"LICENSING := no"/' $RELEASE_SCRIPT
  sed -i 's/"USAGE_STATS := yes"/"USAGE_STATS := no"/'  $RELEASE_SCRIPT
  sed -i 's:/packages_ericsson:/packages_opensource:' $RELEASE_SCRIPT
else
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
  cd $WORKDIR
  #rm -rfv *
  #cp -aRv $GIT_DIR/titan .
  #not verbose:
  rm -rf *
  cp -aR $GIT_DIR/titan .
  cd titan
  pwd
  git reset --hard $GIT_TAG
  rm -f MakefileFOSS.cfg
  sed -i 's/"LICENSING := no"/"LICENSING := yes"/' $RELEASE_SCRIPT
  sed -i 's/"USAGE_STATS := no"/"USAGE_STATS := yes"/' $RELEASE_SCRIPT
  sed -i 's:/packages_opensource:/packages_ericsson:' $RELEASE_SCRIPT
fi
###