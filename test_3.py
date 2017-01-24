#-*- coding:utf-8 -*-

"""目的：为了测试类中全局变量的值是否会在新创建的实例中存在"""

def test_insert(num, l):
    i, j = 0, len(l)
    print "first: ", i, j
    while i < j:
        m = (i+j)//2
        m_data = l[m]
        print "middle data: ",m, m_data, i,j
        if num > m_data:
            i = m + 1
        elif num < m_data:
            j = m -1
        elif i < j:
            l.insert()
        else:
            print "break ",m, num
            l.insert(m, num)
            break
    print l

if __name__ == '__main__':
    l = [1,2,2,45,22,7,55,42]
    l = sorted(l)
    print "start------------"
    print test_insert(34, l)
    print test_insert(3, l)