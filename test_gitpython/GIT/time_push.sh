#!/usr/bin/env bash
set -o xtrace
WORK_DIR='/root/git/test'
SRC_DIR='/root/git/temp'
TMP_DIR='/root/git/.tmp'
CURRENT_DIR=$(cd $(dirname "$0") && pwd)
TIME_FLAG=`date '+%Y-%m-%d %H:%M:%S'`
echo "current time $TIME_FLAG"

create_file(){
    echo "start create dir $TMP_DIR"
    if [ -d "$TMP_DIR" ]; then
        rm -rf $TMP_DIR
    fi
    mkdir -p "$TMP_DIR"
    echo "create dir $TMP_DIR success"
}

copy_file(){
    echo "start copy file '$SRC_DIR' to '$TMP_DIR'"

    if [ -d "$SRC_DIR" ]; then
        cp -Rf $SRC_DIR/* $TMP_DIR/
    else
        echo "not found $SRC_DIR"
        exit 1
    fi
    echo "copy file end"
}

clean_file(){
    echo "into clean file"
    rm $TMP_DIR/.git -rf
    echo "end clean file"
}

move_file(){
    echo "into move file"
    cd $WORK_DIR
    mv $TMP_DIR/* . -f
}

push_file(){
    # echo -e "wangfangjie\npdmi1234\n" > $TMP_DIR/.auth
    expect $CURRENT_DIR/push_auth.ex
}

commit_file(){
    echo "push file to remote server"
    cd $WORK_DIR
    git add -A
    git commit -m '$TIME_FLAG'
    push_file
    echo "push file end"
}


main(){
    echo "----- start main func -----"
    create_file
    copy_file
    clean_file
    move_file
    commit_file
    exit 0
    echo "----- end main func -----"
}
main