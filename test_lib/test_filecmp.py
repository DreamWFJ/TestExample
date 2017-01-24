# -*- coding: utf-8 -*-
import os, sys
import filecmp
import re
import shutil

holderlist = []

def get_abspath(target):
    """
        获取target的完整路径
    """
    return os.path.abspath(target)

def add_path(dst_path, src):
    """
        将src添加到dst_path所在的路径中
    """
    return os.path.join(dst_path, src)

def compareme(src_dir, dst_dir, is_full_path=True):
    """
        比较src_dir与dst_dir中的文件差异，并返回只存在于src_dir目录和只在dst_dir目录的文件
        注意：这里要求传入的src_dir与dst_dir是完整的路径？
    """
    if not is_full_path:
        src_dir = get_abspath(src_dir)
        dst_dir = get_abspath(dst_dir)
    dircomp=filecmp.dircmp(src_dir, dst_dir)
    only_in_one = dircomp.left_only
    diff_in_one = dircomp.diff_files
    common_dirs = dircomp.common_dirs
    [holderlist.append(add_path(src_dir, x)) for x in only_in_one]
    [holderlist.append(add_path(src_dir, x)) for x in diff_in_one]
    if len(common_dirs) > 0:
        for item in common_dirs:
            compareme(add_path(src_dir, item), add_path(dst_dir, item))
    print "compare result: ",holderlist
    return holderlist

def perfect_path(d_path):
    if not d_path.endswith('/'):
        d_path = "%s/"%d_path
    return d_path

def same_as(src_dir, dst_dir):
    # 获取只存在于src_dir和dst_dir各自目录的文件
    src_dir = get_abspath(src_dir)
    dst_dir = get_abspath(dst_dir)
    source_files = compareme(src_dir, dst_dir)
    destination_files = []
    createdir_bool = False

    # 该循环主要用于在dst_dir中创建src_dir才有的目录
    for item in source_files:
        destination_dir = re.sub(src_dir, dst_dir, item)
        destination_files.append(destination_dir)
        if os.path.isdir(item):
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
                createdir_bool = True

    # 重新获取
    if createdir_bool:
        destination_files = []
        source_files = compareme(src_dir, dst_dir)
        [destination_files.append(re.sub(src_dir, dst_dir, item)) for item in source_files]

    copy_pair = zip(source_files, destination_files)
    [shutil.copyfile(item[0], item[1]) for item in copy_pair if os.path.isfile(item[0])]
    print "change content: ",source_files
    return source_files



def main():
    if len(sys.argv) > 2:
        dir1 = sys.argv[1]
        dir2 = sys.argv[2]
    else:
        print "--------"
        sys.exit()
    same_as(dir1, dir2)
    # source_files = compareme(dir1, dir2)
    # dir1 = get_abspath(dir1)
    # dir2 = get_abspath(perfect_path(dir2))
    # destination_files = []
    # createdir_bool = False
    # print "dir1 : ",dir1
    # print "dir2 : ", dir2
    # for item in source_files:
    #     print item
    #     destination_dir = re.sub(dir1, dir2, item)
    #     print "destination_dir = ",destination_dir
    #     destination_files.append(destination_dir)
    #     if os.path.isdir(item):
    #         if not os.path.exists(destination_dir):
    #             os.makedirs(destination_dir)
    #             createdir_bool = True
    # if createdir_bool:
    #
    #     destination_files = []
    #     source_files = []
    #     source_files = compareme(dir1, dir2)
    #     for item in source_files:
    #         destination_dir = re.sub(dir1, dir2, item)
    #         destination_files.append(destination_dir)
    #
    # print "update item:"
    # print source_files
    # copy_pair = zip(source_files, destination_files)
    # print "===---",copy_pair
    # for item in copy_pair:
    #     if os.path.isfile(item[0]):
    #         shutil.copyfile(item[0], item[1])

if __name__ == '__main__':
    main()