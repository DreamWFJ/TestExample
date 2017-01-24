# -*- coding: UTF-8 -*-
import paramiko
import datetime
import os, sys
import logging
import multiprocessing

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
former = logging.Formatter('[%(levelname)-10s] %(asctime)s - (%(threadName)-10s) - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(former)
logger.addHandler(ch)

DEBUG = True
# 这里设置全局的日志模式，可以影响到 paramiko中的日志设置
if DEBUG:
    logging.basicConfig(
        level=logging.DEBUG,
        filename='debug.log',
        filemode='w',
        former= '[%(levelname)-10s] %(asctime)s - (%(threadName)-10s) - %(message)s',
    )

# 判断当前系统是否为 Windows
IS_WIN = os.name == 'nt'

# 获取当前脚本的路径
def get_current_path():
    return sys.path[0]

# 获取当前日期
def get_current_date():
    d = datetime.date.today()
    return "%s-%s-%s" %(d.year, d.month, d.day)

# 拼凑文件完整路径，其中d是完整目录，ip指定文件名，这里ip命名
def make_file_name(d, ip):
    filename = "%s/%s" %(d, ip)
    if IS_WIN:
        filename = filename.replace('/', '\\')
    return filename

# 获取保存的目录
def get_save_path():
    save_path = "%s/%s" %(get_current_path(), get_current_date())
    if IS_WIN:
        save_path = save_path.replace('/', '\\')
    return save_path

# 从txt文件中获取需要处理的ip username, password 列表
def get_ip_list(filename):
    ips_list = []
    try:
        with open(filename, 'r') as data:
            for line in data:
                ip, user, passwd = line.split()
                ips_list.append((ip.strip(), user.strip(), passwd.strip()))

    except IOError, e:
        logger.error('Read file: %s error, Details: %s', filename, str(e))

    except Exception, e:
        logger.error('Handle file: %s content error, Details: %s', filename, str(e))

    return ips_list

# 目录不存在时则创建目录
def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def make_args(a, b):
    l = list(a)
    l.append(b)
    return l

def run():
    # 存放创建的进程和进程处理的Ip的元组列表
    p_l = []
    try:
        save_path = get_save_path()
        create_dir(save_path)
        ips_list = get_ip_list('ip_file.txt')

        for ips in ips_list:
            save_file_path = make_file_name(save_path, ips[0])
            # 将保存的文件的完整路径名称加入到传递给进程的参数中
            args = tuple(make_args(ips, save_file_path))
            p = multiprocessing.Process(target=ssh2, args=args)
            p_l.append((p, ips[0]))
        for p, ip in p_l:
            p.start()
        for p, ip in p_l:
            # 等待5秒钟，一般情况下子进程已经获取到该获取的信息，否则出现异常
            p.join(5)
        for p, ip in p_l:
            # 若还存活，则将该进程终结，并报告抓取失败
            if p.is_alive():
                logger.info('IP: %-16s is Failed', ip)
                p.terminate()
            else:
                logger.info('IP: %-16s is OK', ip)
    except (KeyboardInterrupt, SystemExit):
        for i in p_l:
            i.terminate()
        sys.exit()
    except Exception, e:
        logger.error(str(e))
        sys.exit()


def ssh2(ip, username, password, save_file_path):
    pid = multiprocessing.current_process().pid
    logger.info('Process ID [ %-8s ] handling IP: %-16s', pid, ip)
    try:
        # paramiko.util.log_to_file('paramiko.log')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 这里将超时时间设置长些，以便在主进程中指定的等待时间之后，认为该进程抓取失败
        ssh.connect(ip, 22, username, password, timeout=30)
        logger.debug('Process ID [ %-8s ] send cmd: "dis cur" to %s', pid, ip)
        i, o, e = ssh.exec_command('dis cur')
        i.write("Y")
        with open(save_file_path, 'w') as f:
            f.write("".join(o.readlines()))

    except Exception, e:
        logger.error('Process ID [ %-8s ] IP: %-16s is Failed, Details: %s', pid, ip, str(e))








if __name__=='__main__':
    run()
