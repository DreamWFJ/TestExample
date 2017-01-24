# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_1.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-05 14:52
# ===================================

import socket, select


'''
POLL
    select.poll()，返回一个poll的对象，支持注册和注销文件描述符。

    poll.register(fd[, eventmask])注册一个文件描述符，注册后，可以通过poll()方法来检查是否有对应的I/O事件发生。fd可以是i 个整数，或者有返回整数的fileno()方法对象。
    如果File对象实现了fileno()，也可以当作参数使用。

    eventmask是一个你想去检查的事件类型，它可以是常量POLLIN, POLLPRI和 POLLOUT的组合。如果缺省，默认会去检查所有的3种事件类型。

    事件常量	意义
    POLLIN	有数据读取
    POLLPRT	有数据紧急读取
    POLLOUT	准备输出:输出不会阻塞
    POLLERR	某些错误情况出现
    POLLHUP	挂起
    POLLNVAL	无效请求:描述无法打开
    poll.modify(fd, eventmask) 修改一个已经存在的fd，和poll.register(fd, eventmask)有相同的作用。如果去尝试修改一个未经注册的fd，会引起一个errno为ENOENT的IOError。
    poll.unregister(fd)从poll对象中注销一个fd。尝试去注销一个未经注册的fd，会引起KeyError。
    poll.poll([timeout])去检测已经注册了的文件描述符。会返回一个可能为空的list，list中包含着(fd, event)这样的二元组。 fd是文件描述符， event是文件描述符对应的事件。
    如果返回的是一个空的list，则说明超时了且没有文件描述符有事件发生。timeout的单位是milliseconds，如果设置了timeout，系统将会等待对应的时间。
    如果timeout缺省或者是None，这个方法将会阻塞直到对应的poll对象有一个事件发生。
'''

'''
EPOLL
    在linux2.6（准确来说是2.5.44）由内核直接支持的方法。epoll解决了select和poll的缺点。

    对于第一个缺点，epoll的解决方法是每次注册新的事件到epoll中，会把所有的fd拷贝进内核，而不是在等待的时候重复拷贝，保证了每个fd在整个过程中只会拷贝1次。
    对于第二个缺点，epoll没有这个限制，它所支持的fd上限是最大可以打开文件的数目，具体数目可以cat /proc/sys/fs/file-max查看，一般来说这个数目和系统内存关系比较大。
    对于第三个缺点，epoll的解决方法不像select和poll每次对所有fd进行遍历轮询所有fd集合，而是在注册新的事件时，为每个fd指定一个回调函数，当设备就绪的时候，
        调用这个回调函数，这个回调函数就会把就绪的fd加入一个就绪表中。（所以epoll实际只需要遍历就绪表）。
    epoll同时支持水平触发和边缘触发：

        水平触发（level－triggered）：只要满足条件，就触发一个事件(只要有数据没有被获取，内核就不断通知你)。e.g:在水平触发模式下，
            重复调用epoll.poll()会重复通知关注的event，直到与该event有关的所有数据都已被处理。(select, poll是水平触发, epoll默认水平触发)
        边缘触发（edge－triggered）：每当状态变化时，触发一个事件。e.g:在边沿触发模式中，epoll.poll()在读或者写event在socket上面发生后，将只会返回一次event。
            调用epoll.poll()的程序必须处理所有和这个event相关的数据，随后的epoll.poll()调用不会再有这个event的通知。

    select.epoll([sizehint=-1])返回一个epoll对象。


    事件常量	意义
    EPOLLIN	读就绪
    EPOLLOUT	写就绪
    EPOLLPRI	有数据紧急读取
    EPOLLERR	assoc. fd有错误情况发生
    EPOLLHUP	assoc. fd发生挂起
    EPOLLRT	设置边缘触发(ET)（默认的是水平触发）
    EPOLLONESHOT	设置为 one-short 行为，一个事件(event)被拉出后，对应的fd在内部被禁用
    EPOLLRDNORM	和 EPOLLIN 相等
    EPOLLRDBAND	优先读取的数据带(data band)
    EPOLLWRNORM	和 EPOLLOUT 相等
    EPOLLWRBAND	优先写的数据带(data band)
    EPOLLMSG	忽视
    epoll.close()关闭epoll对象的文件描述符。
    epoll.fileno返回control fd的文件描述符number。
    epoll.fromfd(fd)用给予的fd来创建一个epoll对象。
    epoll.register(fd[, eventmask])在epoll对象中注册一个文件描述符。（如果文件描述符已经存在，将会引起一个IOError）
    epoll.modify(fd, eventmask)修改一个已经注册的文件描述符。
    epoll.unregister(fd)注销一个文件描述符。
    epoll.poll(timeout=-1[, maxevnets=-1])等待事件，timeout(float)的单位是秒（second）。
'''
def test_1():
    EOL1 = b'\n\n'
    EOL2 = b'\n\r\n'
    response  = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
    response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
    response += b'Hello, world!'

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('0.0.0.0', 8080))
    serversocket.listen(1)
    serversocket.setblocking(0)

    epoll = select.epoll()
    epoll.register(serversocket.fileno(), select.EPOLLIN)

    try:
        connections = {}; requests = {}; responses = {}
        while True:
            events = epoll.poll(1)
            for fileno, event in events:
                if fileno == serversocket.fileno():
                    connection, address = serversocket.accept()
                    connection.setblocking(0)
                    epoll.register(connection.fileno(), select.EPOLLIN)
                    connections[connection.fileno()] = connection
                    requests[connection.fileno()] = b''
                    responses[connection.fileno()] = response
                elif event & select.EPOLLIN:
                    requests[fileno] += connections[fileno].recv(1024)
                    if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                        epoll.modify(fileno, select.EPOLLOUT)
                        print('-'*40 + '\n' + requests[fileno].decode()[:-2])
                elif event & select.EPOLLOUT:
                    byteswritten = connections[fileno].send(responses[fileno])
                    responses[fileno] = responses[fileno][byteswritten:]
                    if len(responses[fileno]) == 0:
                        epoll.modify(fileno, 0)
                        connections[fileno].shutdown(socket.SHUT_RDWR)
                elif event & select.EPOLLHUP:
                    epoll.unregister(fileno)
                    connections[fileno].close()
                    del connections[fileno]
    finally:
        epoll.unregister(serversocket.fileno())
        epoll.close()
        serversocket.close()


if __name__ == '__main__':
    test_1()
    