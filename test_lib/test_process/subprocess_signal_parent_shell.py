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

proc = subprocess.Popen(['sh', script_file.name],
                        close_fds=True)
print "PARENT       : Pausing before signaling %s..." % proc.pid
sys.stdout.flush()
time.sleep(1)
print "PARENT       : Signaling child %s..." % proc.pid
sys.stdout.flush()
os.kill(proc.pid, signal.SIGUSR1)
time.sleep(3)