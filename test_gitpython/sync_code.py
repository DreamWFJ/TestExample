# -*- coding: utf-8 -*-

'''
命令行指令
    克隆此存储库
        git clone http://10.100.13.22:8080/tfs/CloudCollection/IaasPlatform/_git/test1
    推送现有存储库
        git remote add origin http://10.100.13.22:8080/tfs/CloudCollection/IaasPlatform/_git/test1
        git push -u origin --all
'''

import pexpect
import os
import shutil
import logging
import logging.handlers
from apscheduler.schedulers.blocking import BlockingScheduler

LOG_FILENAME = 'sync_code.log'
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)
# 设置文件超过1024*1024byte时轮转
rh = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=1048576, backupCount=100
)
rh.setFormatter(formatter)
logger.addHandler(rh)

# 添加一个控制台输出的日志信息
ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)
logger.addHandler(ch)




current_path = os.getcwd()

print current_path

test_url = 'http://10.100.13.22:8080/tfs/CloudCollection/IaasPlatform/_git/test'


def capture_and_promote(pexpect_handler, prompt_info, send_info):
    logger.debug("prompt_info == %s" %prompt_info)
    logger.debug("send_info == %s" %send_info)
    try:
        pexpect_handler.expect(prompt_info)
        pexpect_handler.sendline(send_info)
    except pexpect.TIMEOUT, e:
        ErrorLog = "Cast a TimeOut expection"
        print "e == ", e
        print "ErrorLog == ",ErrorLog
    except Exception, e:
        print "exception: e == ",e


def extend_match(s):
    return "(?i)%s .*: " %s


def git_clone(resource_url, username, password, save_path=None):
    cmd = "git clone %s %s" %(resource_url, save_path)
    logger.info("start clone")
    logger.debug("ARGES: cmd = %s"%cmd)
    logger.debug("ARGES: username = %s"%username)
    logger.debug("ARGES: password = %s"%password)
    logger.debug("ARGES: save_path = %s"%save_path)
    child = pexpect.spawn(cmd)
    capture_and_promote(child, extend_match("username"), username)
    capture_and_promote(child, extend_match("password"), password)
    result = child.readlines()
    s = "".join(result)
    logger.info(s.replace(r"\r\n", r"\n"))
    child.expect(pexpect.EOF)
    logger.info("end clone")

def put_code_to_tfs():
    '''
    git remote add origin http://10.100.13.22:8080/tfs/CloudCollection/IaasPlatform/_git/test1
        git push -u origin --all
    '''
    if not os.path.isdir("%s/appdev "%current_path):
        git_clone("tfs_resource", "wangfangjie", "pdmi1234", "%s/appdev "%current_path)
    os.chdir("%s/.temp/appdev "%current_path)
    os.system("find . -name .git* | xargs rm -rf")
    shutil.copyfile("$SRC_DIR", "$WORK_DIR")
    os.chdir("work_dir")
    commit_dir = []
    for parent, dirname, _ in os.walk("a"):
        os.chdir(os.path.join(parent, dirname))
        os.system("git add -A; git commit -am '$TIME_FLAG'")
        child = pexpect.spawn("git push -u origin --all")
        capture_and_promote(child, extend_match("username"), username)
        capture_and_promote(child, extend_match("password"), password)
        child.expect(pexpect.EOF)
        # commit_dir.append(os.path.join(parent, dirname))
    shutil.rmtree(".temp")

def run():
    logger.info("starting call shell script, sync git code to tfs")
    git_clone(test_url, "wangfangjie", "pdmi1234", "%s/test "%current_path)
    logger.info("finished execute shell script, wait the next time")



def main():
    logger.info("starting time sync task")
    scheduler = BlockingScheduler()
    scheduler.add_job(run, 'cron', hour='1')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit), e:
        logger.warning("catch a exception, and exit")
        scheduler.shutdown()
    logger.info("stopping time sync task")

if __name__ == '__main__':
    # main()
    run()