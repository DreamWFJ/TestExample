# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_1.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-11 14:09
# ===================================



import tablib
headers = (u"姓名", u"性别", u"年龄")
info = [
    (u"李磊", u"男", u"20"),
    (u"王艳", u"女", u"18"),
]
data = tablib.Dataset(*info, headers=headers)

#然后就可以通过下面这种方式得到各种格式的数据了。
data.xlsx
data.xls
data.ods
data.yaml
data.csv
data.tsv
data.html
file('test.xls', 'w').write(data.xls)
#增加行
data.append([u'小明', u'男',18])
#增加列
data.append_col([22, 20,13], header=u'年龄')
print data.csv
#
# #删除行
# del data[1:3]
# #删除列
# del data[u'年龄']
# print data.csv
# #导出excel表
# open('xxx.xls', 'wb').write(data.xls)
# #多个sheet的excel表
# book = tablib.Databook((data1, data2, data3))
# book.xls