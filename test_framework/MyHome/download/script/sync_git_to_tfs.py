# -*- coding: utf-8 -*-
'''
    在sync.conf中使用oslo_config获取配置，有一个小bug，sync区域中的每一项，字典中的密码不能含有逗号，因为键值对默认是以逗号分隔的
'''
import pexpect
import os, sys
import filecmp
import shutil
import logging
import subprocess
import logging.handlers
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from oslo_config import cfg


# 添加默认的配置项，这样即使在没有配置文件的时候也能够正常运行
git_opts = [
    cfg.StrOpt('user_name',
               default='wangfangjie',
               help='git config --global user.name <name>'),
    cfg.StrOpt('user_email',
               default='wangfangjie@pdmi.cn',
               help='git config --global user.email <email>'),
]
git_group = cfg.OptGroup(name='git', title='git options')

log_opts = [
    cfg.StrOpt('file_name',
               default='wangfangjie',
               help='log config file name'),
    cfg.IntOpt('backup_count',
               default=100,
               help='max backup count'),
    cfg.IntOpt('max_bytes',
               default=1048576,
               help='single file max size bytes'),
    cfg.StrOpt('log_formatter',
               default='%(asctime)s - %(levelname)s - %(message)s',
               help='log formatter'),
    cfg.IntOpt('log_level',
               default=logging.DEBUG,
               help='log level'),
]
log_group = cfg.OptGroup(name='log', title='log options')

sync_opts = [
    cfg.DictOpt('sync_1',
                default={
                    'src_url': 'http://10.100.13.235:18080/awcloud/appdev.git',
                    'src_username': 'root',
                    'src_password': 'pdmi,1234567890',
                    'dst_url': 'http://10.100.13.22:8080/tfs/CloudCollection/IaasPlatform/_git/appdev',
                    'dst_username': 'wangfangjie',
                    'dst_password': 'pdmi1234'},
                help='git sync source and destination config info'),
    cfg.DictOpt('sync_2',
                default={
                    'src_url': 'http://10.100.13.235:18080/awcloud/appdev-dashboard.git',
                    'src_username': 'root',
                    'src_password': 'pdmi,1234567890',
                    'dst_url': 'http://10.100.13.22:8080/tfs/CloudCollection/IaasPlatform/_git/appdev-dashboard',
                    'dst_username': 'wangfangjie',
                    'dst_password': 'pdmi1234'},
                help='git sync source and destination config info'),
]
sync_group = cfg.OptGroup(name='sync', title='sync groups')

sync_1_opts = [
    cfg.URIOpt('src_url',
               default='http://10.100.13.22:8080/tfs/CloudCollection/IaasPlatform/_git/test',
               help='the source url address'),
    cfg.StrOpt('src_username',
               default='wangfangjie',
               help='source url \'s auth username'),
    cfg.StrOpt('src_password',
               default='pdmi1234',
               help='source url \'s auth password'),
    cfg.URIOpt('dst_url',
               default='http://10.100.13.22:8080/tfs/CloudCollection/IaasPlatform/_git/test1',
               help='the destination url address'),
    cfg.StrOpt('dst_username',
               default='wangfangjie',
               help='destination url \'s auth username'),
    cfg.StrOpt('dst_password',
               default='pdmi1234',
               help='destination url \'s auth password'),
]
sync_1_group = cfg.OptGroup(name='sync_1', title='sync_1 groups')



class MyConfigOpts(object):
    def __init__(self, CONF):
        self.CONF = CONF
        for opts, group in [(git_opts, git_group),
                            (log_opts, log_group),
                            (sync_opts, sync_group),
                            (sync_1_opts, sync_1_group)]:
            self._register_opts(opts, group)

    def _register_opts(self, opts, group=None):
        self.CONF.register_opts(opts, group)

    def _load_config(self, filename='sync.conf'):
        self.CONF(default_config_files=[filename])
        return self.CONF



class BeforeGitExecption(Exception):
    pass


class CodeSync(object):
    def __init__(self, config_file=None):
        if config_file is None:
            config_file = 'sync.conf'

        self.config_file = config_file
        self.current_path = os.getcwd()
        self._init_config()
        self._work_dir = "%s/work"%self.current_path
        self._temp_dir = "%s/.temp/"%self.current_path
        self._old_version_dir = "%s/old_version/"%self.current_path
        self._new_file_list = []
        self._is_exist_old_version = False

    def _init_config(self):
        a = MyConfigOpts(cfg.CONF)
        self.conf = a._load_config(self.config_file)
        self.logger = self._init_log_config()
        self._init_git_config()

    def _init_log_config(self):
        logger = logging.getLogger()
        formatter = logging.Formatter(self.conf.log.log_formatter)
        logger.setLevel(self.conf.log.log_level)
        rh = logging.handlers.RotatingFileHandler(
            self.conf.log.file_name, maxBytes=self.conf.log.max_bytes,
            backupCount=self.conf.log.backup_count
        )
        rh.setFormatter(formatter)
        logger.addHandler(rh)

        # 添加一个控制台输出的日志信息
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)
        # logger.warning()
        return logger

    def test_config(self):
        print self.conf.git.user_name
        print self.conf.git.user_email
        print self.conf.log.file_name
        print self.conf.log.log_formatter
        print self.conf.log.max_bytes
        print self.conf.sync_1.src_url
        print self.conf.sync_1.src_username
        print "----------------------"
        print list(self.conf.sync)
        print self.conf.sync['sync_1']
        print self.conf.sync.sync_1['src_password']


    def _init_git_config(self):
        self.execute_system_cmd("git config --global user.name '%s'"%self.conf.git.user_name)
        self.execute_system_cmd("git config --global user.email '%s'"%self.conf.git.user_email)

    def execute_system_cmd(self, cmd):
        subp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        exec_status = subp.wait()
        exec_result = subp.stdout.readlines()
        self.logger.debug("".join(exec_result))
        if exec_status:
            self.logger.warning("execute shell cmd : '%s' failed. return value is: %s, type is: %s."%(cmd, exec_status, type(exec_status)))

        return exec_status

    def get_abspath(self, target):
        """
            获取target的完整路径
        """
        return os.path.abspath(target)

    def add_path(self, dst_path, src):
        """
            将src添加到dst_path所在的路径中
        """
        return os.path.join(dst_path, src)

    def compareme(self, src_dir, dst_dir, is_full_path=True):
        """
            比较src_dir与dst_dir中的文件差异，并返回只存在于src_dir目录和只在dst_dir目录的文件
        """
        if not is_full_path:
            src_dir = self.get_abspath(src_dir)
            dst_dir = self.get_abspath(dst_dir)
        dircomp=filecmp.dircmp(src_dir, dst_dir, ['.babelrc'])
        only_in_one = dircomp.left_only
        diff_in_one = dircomp.diff_files
        common_dirs = dircomp.common_dirs
        [self._new_file_list.append(self.add_path(src_dir, x)) for x in only_in_one]
        [self._new_file_list.append(self.add_path(src_dir, x)) for x in diff_in_one]
        if len(common_dirs) > 0:
            for item in common_dirs:
                self.compareme(self.add_path(src_dir, item), self.add_path(dst_dir, item))
        return self._new_file_list

    def is_need_push(self, old_version_path):
        if not self._is_exist_old_version:
            return True
        self._new_file_list = []
        self.logger.debug("self._temp_dir == %s "%self._temp_dir)
        self.logger.debug("old_version_path == %s "%old_version_path)
        self.compareme(self._temp_dir, old_version_path)
        self.logger.debug("compare %s - %s result: %s"%(self._temp_dir, old_version_path, self._new_file_list))
        self.logger.debug("self._new_file_list == %s "%self._new_file_list)
        if len(self._new_file_list) > 0:
            return True
        return False


    def make_clone_cmd(self, url, save_path=None):
        cmd = "git clone %s %s" %(url, save_path)
        return cmd

    def get_code(self, resource_addr, username=None, password=None, save_path=None):
        cmd = self.make_clone_cmd(resource_addr, save_path)
        self.excute_cmd(cmd, username, password)

    def alter_file(self, src, dst):
        self.execute_system_cmd("find %s -name .git* | xargs rm -rf" %src)
        self.execute_system_cmd("cp -Rf %s/* %s"%(src, dst))

    def save_old_version(self, src, dst):
        self._is_exist_old_version = True
        if not os.path.exists(dst):
            os.makedirs(dst)
            self._is_exist_old_version = False
        self.execute_system_cmd("cp -Rf %s/* %s"%(src, dst))

    def remove_dir(self, path):
        shutil.rmtree(path)

    def add_commit_note(self, note):
        cmd = "git add -A; git commit -am '%s'" %note
        if self.execute_system_cmd(cmd):
            self.logger.warning("not find alter records.")
            raise BeforeGitExecption("execute cmd: '%s' error."%cmd)

    def put_code(self, username=None, password=None):
        self.excute_cmd("git push -u origin --all", username, password)

    def excute_cmd(self, cmd, username, password):
        self.logger.debug("excute cmd: %s"%cmd)
        # 根据命令产生一个子进程
        child = pexpect.spawn(cmd)
        if username and password:
            # 抓取输出流，并根据输出流信息发送用户名和密码
            self.inject_authority(child, self.decorate_expression("username"), username)
            self.inject_authority(child, self.decorate_expression("password"), password)
        # 读出输出流信息，用于写入日志中
        result = child.readlines()
        s = "".join(result)
        self.logger.info(s.replace(r"\r\n", r"\n"))
        # 等待整个cmd命令执行结束
        child.expect(pexpect.EOF)

    def decorate_expression(self, expression):
        # 修改正则表达式，匹配忽略首字母大小写的用户名，密码关键字
        return "(?i)%s .*: " %expression

    def inject_authority(self, pexpect_handler, prompt_info, send_info):
        try:
            # 抓取指定提示信息
            pexpect_handler.expect(prompt_info)
            # 然后发送指定信息
            pexpect_handler.sendline(send_info)
        except pexpect.TIMEOUT, e:
            self.logger.error("catch a TIMEOUT exception: %s"%e)
            ErrorLog = "error authority info: %s -- %s"%(prompt_info, send_info)
            self.logger.error(ErrorLog)
        except Exception, e:
            self.logger.fatal("catch a exception: %s" %e)

    def get_project_name(self, src_url):
        # 根据git资源地址获取项目名称
        s = src_url
        if s.endswith('.git'):
            s = s[:-4]
        l = s.rfind(r'/')
        return s[l+1:]

    def __call__(self):
        self.sync()

    def sync(self):
        self.logger.info("starting sync git code to tfs...")
        # 遍历配置选项中的sync域中的键值对，从而动态获取需要同步的git资源
        for k in list(self.conf.sync):
            sync_item = self.conf.sync[k]
            self.sync_code(sync_item['src_url'], sync_item['src_username'], sync_item['src_password'],
                           sync_item['dst_url'], sync_item['dst_username'], sync_item['dst_password'])

        self.logger.info("sync git code to tfs successfully.")

    def get_current_time(self, delay_time=0):
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time() + delay_time))

    def sync_code(self, src_url, src_username, src_password,
             dst_url, dst_username, dst_password):

        self.logger.debug("src_url == %s"%src_url)
        self.logger.debug("dst_url == %s"%dst_url)

        project_name = self.get_project_name(src_url)
        project_path = "%s/%s/"%(self._work_dir, project_name)
        old_version_path = "%s/%s/"%(self._old_version_dir, project_name)

        self.logger.info("project name: %s"%project_name)
        # 这里的临时目录在程序后面是会删除的
        if not os.path.isdir(self._temp_dir):
            self.get_code(src_url, src_username, src_password, self._temp_dir)
        # 这里是工作目录
        if not os.path.isdir(project_path):
            self.get_code(dst_url, dst_username, dst_password, project_path)
        # 将git clone下的代码删除.git*之后，将其他所有文件拷贝到工作目录
        self.alter_file(self._temp_dir, project_path)
        self.save_old_version(self._temp_dir, old_version_path)
        if self.is_need_push(old_version_path):
            self.logger.debug("temp dir is: %s"%self._temp_dir)
            self.logger.debug("work dir is: %s"%project_path)
            # 切换到项目目录
            os.chdir(project_path)
            try:
                # 添加注释
                self.add_commit_note("timer task commit: %s"%self.get_current_time())
                # 提交代码
                self.put_code(dst_username, dst_password)
            except BeforeGitExecption, e:
                self.logger.error(e)
        else:
            self.logger.info("")
            self.logger.info("==========================================================")
            self.logger.info("<<<<<<<<<<<<<<<<<<< not find new update >>>>>>>>>>>>>>>>>>>>")
            self.logger.info("==========================================================")
            self.logger.info("")
        self.remove_dir(self._temp_dir)


def test():
    '''
    测试配置文件加载后，输出参数信息
    '''
    try:
        sync_instance = CodeSync()
        sync_instance.test_config()
        sync_instance()
    except (KeyboardInterrupt, SystemExit), e:
        print "catch a exception, and exit"
        sys.exit()
    print "stopping time sync task"

def main():
    '''
    程序入口，开启定时执行
    '''
    print "starting time sync task"
    sched = BlockingScheduler()
    sync_instance = CodeSync()
    sched.add_job(sync_instance, 'interval', id="sysn_git_code_to_tfs", hours=24, next_run_time=sync_instance.get_current_time(10))
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit), e:
        print "catch a exception, and exit"
        sched.shutdown()
        sys.exit()
    print "stopping time sync task"


if __name__ == '__main__':
    main()
    # test()