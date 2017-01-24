#!/usr/bin/env bash
set -o xtrace
WORK_DIR='/root/git/project'
SRC_DIR='/root/git/.temp'
CURRENT_DIR=$(cd $(dirname "$0") && pwd)
TIME_FLAG=`date '+%Y-%m-%d %H:%M:%S'`
echo "current time $TIME_FLAG"
USERNAME='root'
PASSWORD='pdmi,1234567890'
APPDEV="http://10.100.13.235:18080/awcloud/appdev.git"
APPDEV_DASHBOARD="http://10.100.13.235:18080/awcloud/appdev-dashboard.git"



create_dir(){
    if [ -d "$SRC_DIR" ]; then
        rm -rf $SRC_DIR
    fi
    mkdir -p "$SRC_DIR"
}

clone_code(){
    create_dir
    cd $SRC_DIR
    expect $CURRENT_DIR/auto_clone_code.ex $APPDEV $USERNAME $PASSWORD
    expect $CURRENT_DIR/auto_clone_code.ex $APPDEV_DASHBOARD $USERNAME $PASSWORD
}

delete_git(){
    cd $SRC_DIR
    find . -name .git* | xargs rm -rf
}

copy_file(){
    if [ -d "$SRC_DIR" ]; then
        delete_git
        cp -Rf $SRC_DIR/* $WORK_DIR/
    else
        echo "not found $SRC_DIR"
        exit 1
    fi
}


push_file(){
    expect $CURRENT_DIR/push_to_remote.ex
}

commit_file(){
    cd $WORK_DIR
    for dir in $(ls -l | awk '/^d/ {print $NF}'); do
        cd $dir
        git add -A
        git commit -am '$TIME_FLAG'
        push_file
        cd ..
    done
    
}


main(){
    echo "----- start main func -----"
    clone_code
    copy_file
    commit_file
    exit 0
    echo "----- end main func -----"
}


main