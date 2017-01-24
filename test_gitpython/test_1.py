from __future__ import print_function

from __future__ import absolute_import

import pexpect
import getpass, os, traceback
def ssh_command (user, host, password, command):
     ssh_newkey = 'Are you sure you want to continue connecting'
     child = pexpect.spawn('ssh -l %s %s %s'%(user, host, command))
     i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
     if i == 0: # Timeout
         print('ERROR!')
         print('SSH could not login. Here is what SSH said:')
         print(child.before, child.after)
         return None
     if i == 1: # SSH does not have the public key. Just accept it.
         child.sendline ('yes')
         child.expect ('password: ')
         i = child.expect([pexpect.TIMEOUT, 'password: '])
         if i == 0: # Timeout
             print('ERROR!')
             print('SSH could not login. Here is what SSH said:')
             print(child.before, child.after)
             return None
     child.sendline(password)
     return child

def main ():
     host = "www.example.com"
     user = "root"
     password = "password"
     child = ssh_command (user, host, password, '/bin/ls -l')
     child.expect(pexpect.EOF)
     print(child.before)

if __name__ == '__main__':
     try:
         main()
     except Exception as e:
         print(str(e))
         traceback.print_exc()
         os._exit(1)