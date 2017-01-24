#-*- coding:utf-8 -*-
import git
import sys
import os
import time

class MyProgressPrinter(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(op_code, cur_count, max_count, cur_count / (max_count or 100.0), message or "NO MESSAGE")

pi = os.pipe()
sys.stdin = pi[0]
os.write(pi[1], "wangfangjie")
os.write(pi[1], "\n")
time.sleep(1)

os.write(pi[1], "pdmi1234")
os.write(pi[1], "\n")


repo_url = "http://10.100.13.22:8080/tfs/CloudCollection/IaasPlatform/_git/test"
repo = git.Repo.clone_from(repo_url, '/root/git/', progress=MyProgressPrinter())
heads = repo.heads
print heads
os.close(pi[0])
os.close(pi[1])
print 'end ----------'