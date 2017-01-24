# -*- coding: utf-8 -*-
import subprocess

def test_1():
    subprocess.call(['ls', '-l'])

def test_2():
    # 重新开启一个shell执行命令，默认返回值为程序的退出码
    subprocess.call('echo $HOME', shell=True)

def test_3():
    try:
        # 类似于call，只是如果出错，则产生CallProcessError异常
        subprocess.check_call(['false'])
    except subprocess.CalledProcessError as err:
        print "ERROR:", err

def test_4():
    # 捕获输出信息
    output = subprocess.check_output(['ls', '-l'])
    print 'Have %d bytes in output' % len(output)
    print output

def test_5():
    try:
        # 将标准错误输出至控制台
        output = subprocess.check_output(
            'echo to stdout; echo to stderr 1>&2; exit 1',
            shell=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as err:
        print "ERROR:", err
    else:
        print 'Have %d bytes in output' % len(output)
        print output

def test_6():
    print 'read:'
    # 将输出数据重定向到管道中
    proc = subprocess.Popen(['echo', '"to stdout"'],
                            stdout=subprocess.PIPE,
                            )
    stdout_value = proc.communicate()[0]
    print '\tstdout:',repr(stdout_value)

def test_7():
    print 'write:'
    # 从管道中读取
    proc = subprocess.Popen(['cat', '-'],
                            stdin=subprocess.PIPE,
                            )
    proc.communicate('\tstdin: to stdin wfj\n')

def test_8():
    print 'popen2'
    # 将输出数据重定向到管道中,或从管道中读取
    proc = subprocess.Popen(['cat', '-'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            )
    msg = 'through stdin to stdout'
    stdout_value = proc.communicate(msg)[0]
    print '\tpass through:',repr(stdout_value)

def test_9():
    print 'popen3:'
    proc = subprocess.Popen('cat -; echo "to stderr" 1>&2',
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            )
    msg = 'through stdin to stdout'
    stdout_value, stderr_value = proc.communicate(msg)
    print '\tpass through:',repr(stdout_value)
    print '\tstderr      :',repr(stderr_value)

def test_10():
    print 'popen3:'
    proc = subprocess.Popen('cat -; echo "to stderr" 1>&2',
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            )
    msg = 'through stdin to stdout'
    stdout_value, stderr_value = proc.communicate(msg)
    print '\tpass through:',repr(stdout_value)
    print '\tstderr      :',repr(stderr_value)

def test_11():
    # 连接多个管道
    cat = subprocess.Popen(['cat', 'README.rst'],
                           stdout=subprocess.PIPE,
                           )
    grep = subprocess.Popen(['grep', 'http:'],
                            stdin=cat.stdout,
                            stdout=subprocess.PIPE,
                            )

    cut = subprocess.Popen(['cut', '-f', '3', '-d:'],
                           stdin=grep.stdout,
                           stdout=subprocess.PIPE,
                           )

    end_of_pipe = cut.stdout
    print 'Included files:'
    for line in end_of_pipe:
        print '\t', line.strip()

if __name__ == '__main__':
    # test_1()
    # test_2()
    # test_3()
    # test_4()
    # test_5()
    # test_6()
    # test_7()
    # test_8()
    # test_9()
    # test_10()
    test_11()