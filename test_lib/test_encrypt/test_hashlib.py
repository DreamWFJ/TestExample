# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_hashlib.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-20 14:07
# ===================================

import hashlib

lorem = '''
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
    implied.  See the License for the specific language governing
    permissions and limitations under the License.'''

def test_1():
    # 计算MD5散列或者摘要
    h = hashlib.md5()
    h.update(lorem)
    print 'MD5:     ', h.hexdigest()

    #SHA1摘要
    h1 = hashlib.sha1()
    h1.update(lorem)
    print 'SHA1:    ', h1.hexdigest()


def test_2(hash_name, data):
    # 指定哈希方式：sha1, sha256, sha512, md去取数据data的哈希值
    h = hashlib.new(hash_name)
    h.update(data)
    print h.hexdigest()

if __name__ == '__main__':
    test_1()
    