# -*- coding: utf-8 -*-
import tempfile
import os
import subprocess
import signal
import time
import sys

script = '''#!/bin/sh
echo "Shell script in process $$"
set -x
python signal_child.py
'''

script_file = tempfile.NamedTemporaryFile('wt')
script_file.write(script)
script_file.flush()

# 如果向子进程发送信号但不知道其进程id，可以使用一个进程组关联这些子进程，使他们鞥一起收到信号
# 进程组使用os.setsid()创建，将会话id 设置为当前进程的进程id，所有子进程都会从其父进程继承会话Id，将函数作为preexec_fn的参数传入
# Popen，从而在fork()之后新进程中允许这个函数。向整个进程组发送信号，用os.killpg()
def show_setting_sid():
    print "Calling os.setsid() from %s" % os.getpid()
    sys.stdout.flush()
    os.setsid()

proc = subprocess.Popen(['sh', script_file.name],
                        close_fds=True,
                        preexec_fn=show_setting_sid,
                        )

print "PARENT       : Pausing before signaling %s..." % proc.pid
sys.stdout.flush()
time.sleep(1)
print "PARENT       : Signaling process group %s..." % proc.pid
sys.stdout.flush()
os.killpg(proc.pid, signal.SIGUSR1)
time.sleep(3)