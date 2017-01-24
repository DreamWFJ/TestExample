# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_hmac.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-20 14:07
# ===================================

import hmac
import hashlib
import base64
try:
    import cPickle as pickle
except:
    import pickle
import pprint
from StringIO import StringIO

lorem = '''
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
    implied.  See the License for the specific language governing
    permissions and limitations under the License.'''

def make_digest(message):
    hash = hmac.new('secret-shared-key-goes-here',
                    message,
                    hashlib.sha1)
    return hash.hexdigest()

class SimpleObject(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name


def test_1():
    # 消息hmac签名 -- 默认的MD5散列算法
    digest_maker = hmac.new('secret-shared-key-goes-here')
    digest_maker.update(lorem)
    digest = digest_maker.hexdigest()
    print 'md5散列算法的hmac签名       :',digest

    # 消息hmac签名 -- 采用SHA1散列算法
    digest_maker = hmac.new('secret-shared-key-goes-here', lorem, hashlib.sha1)
    # digest_maker.update(lorem)
    digest = digest_maker.hexdigest()
    print 'sha1散列算法的hmac签名      :',digest
    print 'sha1散列算法的hmac签名base64:',base64.encodestring(digest)

def test_2():
    out_s =StringIO()
    o = SimpleObject('digest matches')
    pickled_data = pickle.dumps(o)
    digest = make_digest(pickled_data)
    header = '%s %s' %(digest, len(pickled_data))
    print 'WRITING: ', header
    out_s.write(header + '\n')
    out_s.write(pickled_data)


if __name__ == '__main__':
    # test_1()
    test_2()
