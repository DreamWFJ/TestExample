from oslo_concurrency import lockutils
from oslo_concurrency import processutils

@lockutils.synchronized('not_thread_safe')
def not_thread_safe():
    "Locking a function (local to a process)"
    pass

@lockutils.synchronized('not_thread_process_safe', external=True)
def not_thread_process_safe():
    "Locking a function (local to a process as well as across process)"
    pass

# Common ways to prefix/namespace the synchronized decorator
myapp_synchronized = lockutils.synchronized_with_prefix("myapp")

"""
Command Line Wrapper

$ lockutils-wrapper env | grep OSLO_LOCK_PATH
OSLO_LOCK_PATH=/tmp/tmpbFHK45
"""