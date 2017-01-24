#!/bin/bash
# Inspired by Debian and RedHat run-parts but portable and specific to di-b.
#
# Copyright 2012 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# 总的来说：该脚本是执行dib-run-parts --list dir 或 dib-run-part dir后运行dir目录中的脚本，这些脚本都是以
# 数字开头的，以从小到大的顺序执行，执行之前会去先加载该目录同级的environment.d目录下的环境设置（若有则加载）  ---wfj


# 下面表示获取环境变量RUN_PARTS_REGEX的值，若环境变量为空或者未定义则返回后面的正则表达式
allowed_regex=${RUN_PARTS_REGEX:-"^[0-9A-Za-z_-]+$"}
show_list=
# 下面表示一旦某个命令执行结果异常则退出，并且取消所有的变量设置
set -ue
# 下面表示返回最后一个非零退出的命令执行状态，默认是返回最后一条命令的执行状态，中间可能有执行失败的
set -o pipefail

# 获取脚本名称，去掉了路径，还可以获取脚本目录，通过命令dirname $0
name=$(basename $0)

usage() {
    echo "Usage: $name [OPTION] scripts_directory"
    echo "Option:"
    echo "      --list  print names of all valid files"
    echo
    echo "Examples:"
    echo "      dib-run-parts --list /opt/stack/os-config-refresh/configure.d/"
    echo "      dib-run-parts /opt/stack/os-config-refresh/configure.d/"
    exit 1
} >&2

# $() 这种方式是新开一个进程执行括号中的命令，然后返回执行结果
output_prefix() {
    printf "%s %s " "${name}" "$(date)" >&2
}
# $* 中的参数是整个作为一个字符串，$@中的参数是各自为一个字符串
output () {
    output_prefix
    echo $* >&2
}

output_printf () {
#    local表示设置局部变量
    local FORMAT="$1"
#    shift表示左移参数，若$1是默认的第一个参数，则移动后$1=$2, $2=$3 ...
    shift
    output_prefix
    printf "${FORMAT}" $@ >&2
}

# source the environment files from environment.d
#  arg : target_dir
source_environment() {
#   $target_dir/../environment.d 表示将$target_dir目录的上一级中的environment.d的路径赋值给dir
    local dir=$target_dir/../environment.d
    local env_files
    local xtrace
#    测试 ${dir}是否是目录，是则执行if内的命令
    if [ -d ${dir} ] ; then
#       在${dir}目录中查找类型为文件，查找深度为1，即不进入子目录，然后将结果通过管道传递到grep中，获取满足正则表达式的结果
#       再通过管道传递给下一级处理，LANG=C是去本地化设置，按照国际标准重置语言环境，LC_ALL=C和LANG=C一样
        env_files=$(find ${dir} -maxdepth 1 -xtype f | \
                           grep -E "/[0-9A-Za-z_\.-]+$" | \
                           LANG=C sort -n)
        for env_file in $env_files ; do
            output "Sourcing environment file ${env_file}"
            # Set tracing as we import these environment files; it's
            # nice to see the definitions in the logs
#            set +o 显示当前开启和关闭设置的状态，常见项通过help set中的-o可以知道，下面这句话表示获取xtrace的默认状态
            xtrace=$(set +o | grep xtrace)
#            开启显示执行命令，前面有一个+号
            set -o xtrace
            source $env_file
#            恢复默认xtrace的状态
            $xtrace
        done
    fi
}
# 如果参数个数小于1则输出帮助信息，并退出
if [ $# -lt 1 ] ; then
    usage
fi
# 判断第一个参数是否为--list
if [ "$1" == "--list" ] ; then
    show_list="1"
    shift
fi
# 若没有第一个参数则返回空
target_dir="${1:-}"

if ! [ -d "$target_dir" ] ; then
    output "Scripts directory [$target_dir] must exist and be a directory"
    usage
fi

# We specifically only want to sort *by the numbers*.
# Lexical sorting is not guaranteed, and identical numbers may be
# parallelized later
# Note: -maxdepth 1 ensures only files in the target directory (but not
# subdirectories) are run, which is the way run-parts behaves.
# 这里find同上面的解释，只是多加了一个-exec参数，表示根据前面查找的结果执行后面的命令
targets=$(find $target_dir -maxdepth 1 -xtype f -executable -printf '%f\n' | grep -E "$allowed_regex" | LANG=C sort -n || echo "")

if [ "$show_list" == "1" ] ; then
    for target in $targets ; do
        echo "${target_dir}/${target}"
    done
    exit 0
fi

# 创建一个临时目录，并生成一个临时文件profiledir.XXXXX，默认在/tmp目录下
PROFILE_DIR=$(mktemp -d --tmpdir profiledir.XXXXXX)

# note, run this in a sub-shell so we don't pollute our
# own environment with source_environment
(
    source_environment

    for target in $targets ; do
        output "Running $target_dir/$target"
#        ${target//\//_} 表示所有的'/'用'_'替换
        target_tag=${target//\//_}
#        将时间写入临时文件中，这是为后面计算脚本运行时间准备
        date +%s.%N > $PROFILE_DIR/start_$target_tag
        $target_dir/$target
        target_tag=${target//\//_}
        date +%s.%N > $PROFILE_DIR/stop_$target_tag
        output "$target completed"
    done
)

output "----------------------- PROFILING -----------------------"
output ""
output "Target: $(basename $target_dir)"
output ""
output_printf "%-40s %9s\n" Script Seconds
output_printf "%-40s %9s\n" --------------------------------------- ----------
output ""
pushd $PROFILE_DIR > /dev/null
for target in $(find . -name 'start_*' -printf '%f\n' | env LC_ALL=C sort -n) ; do
#   从左边开始扫描target变量，匹配start_，将扫描到的数据全部删除
    stop_file=stop_${target##start_}
    start_seconds=$(cat $target)
    stop_seconds=$(cat $stop_file)
    duration=$(echo - | awk "{ print $stop_seconds - $start_seconds }")
    LC_NUMERIC=C LC_ALL=C output_printf "%-40s %10.3f\n" ${target##start_} $duration
done
popd > /dev/null
rm -rf $PROFILE_DIR
output ""
output "--------------------- END PROFILING ---------------------"
