# -*- coding: utf-8 -*-
# ==================================
# Author        : WFJ
# ScriptName    : example.py
# CreateTime    : 2016-09-17 11:37
# ==================================
# 正则表达式练习


import re

def test_1():
    s = r"/version/user(?=/)(?P<user_id>.*)"
    pattern = re.compile(s)
    for i in ['/version/user/12345',
              '/version/user/fsa',
              '/version/users',
              '/version/user',
              '/version/user//']:
        print 're: %s'%i
        # match会从字符串最前面进行匹配，开始不一样，则匹配失败
        match = pattern.match(i)
        if match:
            print '\t', match.group()
            print '\t',match.groupdict()


def test_2():
    pattern = 'this'
    text = 'Does this text match the pattern?'
    # search在字符串中进行搜索
    match = re.search(pattern, text)
    # 或者字符串的索引位置
    s = match.start()
    e = match.end()
    print 'Found "%s"\n in "%s"\n from %d to %d ("%s")' %\
          (match.re.pattern, match.string, s, e, text[s:e])
    # 打印结果如下
    # Found "this"
    # in "Does this text match the pattern?"
    # from 5 to 9 ("this")

def test_3():
    # 编译表达式为一个RegexObject，会使执行更快
    regexes = [
        re.compile(p)
        for p in ['this', 'that']
    ]
    text = 'Does this text match the pattern?'
    print 'Text : %r\n' % text
    for regex in regexes:
        print 'Seeking "%s" ->' % regex.pattern,
        if regex.search(text):
            print 'match!'
        else:
            print 'no match'


def test_4():
    # 多重匹配
    text = 'abbaaabbbbaaaaa'
    pattern = 'ab'
    # 返回所有而不重叠的字符串
    for match in re.findall(pattern, text):
        print 'findall - Found "%s"' %match
    # 返回一个迭代器
    for match in re.finditer(pattern, text):
        s = match.start()
        e = match.end()
        print 'finditer - Found "%s" at %d:%d' % (text[s:e], s, e)
    # 执行结果为
    # findall - Found "ab"
    # findall - Found "ab"
    # finditer - Found "ab" at 0:2
    # finditer - Found "ab" at 5:7


def test_5():
    # 模式语法
    def test_patterns(text, patterns=[]):
        for pattern, desc in patterns:
            print 'Pattern %r (%s)\n' %(pattern, desc)
            print ' %r' % text
            for match in re.finditer(pattern, text):
                s = match.start()
                e = match.end()
                substr = text[s:e]
                n_backslashes = text[:s].count('\\')
                prefix = '.' * (s + n_backslashes)
                print ' %s%r' %(prefix, substr)
            print
        return

    test_patterns(
        'abbaaabbbbaaaaa',
        [
            ('ab',          "'a' followed by 'b'"),
            ('ab*',         "'a' followed by zero or more 'b'"),
            ('ab+',         "'a' followed by one or more 'b'"),
            ('ab?',         "'a' followed by zero or one 'b'"),
            ('ab{3}',       "'a' followed by three 'b'"),
            ('ab{2,3}',     "'a' followed by two or three 'b'"),
            # 加'?'关闭贪心行为
            ('ab*?',        "'a' followed by zero or more 'b'"),
            ('ab+?',        "'a' followed by one or more 'b'"),
            ('ab??',        "'a' followed by zero or one 'b'"),
            ('ab{3}?',      "'a' followed by three 'b'"),
            ('ab{2,3}?',    "'a' followed by two or three 'b'"),
        ]
    )
    test_patterns(
        'This is some text -- with punctuation.',
        [
            # 字符集
            ('[ab]',        "either 'a' or 'b'"),
            ('a[ab]+',      "'a' followed by 1 or more 'a' or 'b'"),
            ('a[ab]+?',     "'a' followed by 1 or more 'a' or 'b', not greedy"),
            ('[a-z]+',      'sequences of lowercase letters'),
            ('[A-Z]+',      'sequences of uppercase letters'),
            ('[a-zA-Z]+',   'sequences of lowercase or uppercase letters'),
            ('[A-Z][a-z]+', 'one uppercase followed by lowercase'),
        ]
    )
    test_patterns(
        # 贪心模式即在第一次成功匹配之后，继续向后匹配，直到不能匹配为止
        'abbaabbba',
        [
            ('a.',        "'a' followed by any one character"),
            ('b.',        "'b' followed by any one character"),
            ('a.*b',      "'a' followed by anything, ending in 'b'"),
            ('a.*?b',     "'a' followed by anything, ending in 'b'"),
        ]
    )
    test_patterns(
        'A prime #1 example!',
        [
            # 转义码
            (r'\d+',      'sequences of digits'),
            (r'\D+',      'sequences of nondigits'),
            (r'\s+',      'sequences of whitespace'),
            (r'\S+',      'sequences of nonwhitespace'),
            (r'\w+',      'alphanumeric characters'),
            (r'\W+',      'nonalphanumeric'),
        ]
    )
    test_patterns(
        'This is some text -- with punctuation.',
        [
            # 锚定码
            (r'^\w+',       "word at start of string"),
            (r'\A\w+',      'word at start of string'),
            (r'\w+\S*$',    'word at end of string, skip punctuation'),
            (r'\w+\S*\Z',   'word near end of string, skip punctuation'),
            (r'\w*t\w*',    'word containning t'),
            (r'\bt\w+',     't at start of word'),
            (r'\w+t\b',     't at end of word'),
            (r'\Bt\B',      't, not start or end of word'),
        ]
    )
    test_patterns(
        'abbaaabbbbaaaaa.',
        [
            (r'a(ab)',      "a followed by literal ab"),
            (r'a(a*b*)',    'a followed by 0-n a and 0-n b'),
            (r'a(ab)*',     'a followed by 0-n ab'),
            (r'a(ab)+',     'a followed by 1-n ab'),
        ]
    )

def test_6():
    text = 'This is some text -- with punctuation.'
    print 'Input text               :',text
    regex = re.compile(r'(\bt\w+)\W+(\w+)')
    print 'Pattern                  :',regex.pattern
    match = regex.search(text)
    print 'Entire match             :', match.group(0)
    print 'Word starting with "t"   :', match.group(1)
    print 'Word after with "t" word :', match.group(2)

def test_7():
    # 命名组
    text = 'This is some text -- with punctuation.'
    print 'Input text               :',text
    for pattern in [
        r'^(?P<first_word>\w+)',
        r'(?P<last_word>\w+)\S*$',
        r'(?P<t_word>\bt\w+)\W+(?P<other_word>\w+)',
        r'(?P<ends_with_t>\w+t)\b',
    ]:
        regex = re.compile(pattern)
        match = regex.search(text)
        print 'Pattern                  :', regex.pattern
        print 'Entire match             :', match.groups()
        print 'Match dict               :', match.groupdict()
        print

def test_8():
    def test_patterns(text, patterns=[]):
        for pattern, desc in patterns:
            print 'Pattern %r (%s)\n' %(pattern, desc)
            print 'Input text: %r' % text
            for match in re.finditer(pattern, text):
                s = match.start()
                e = match.end()
                prefix = ' ' * (s)
                print 'prepare: %s%r%s' %(prefix, text[s:e], ' '*(len(text)-e))
                print match.groups()
                if match.groupdict():
                    print '%s%s' % (' ' * (len(text) - s), match.groupdict())
            print
        return
    test_patterns(
        'abbaabbba',
        [
            (r'a((a*)(b*))',    'a followed by 0-n a and 0-n b')
        ]
    )
    test_patterns(
        'abbaabbba',
        [
            (r'a((a+)|(b+))',   'a then seq. of a or seq. of b'),
            (r'a((a|b)+)',      'a then seq. of [ab]'),
        ]
    )
    test_patterns(
        # 非捕获组
        'abbaabbba',
        [
            (r'a((?:a+)|(?:b+))',   'a then seq. of a or seq. of b'),
        ]
    )

def test_9():
    # 添加搜索选项--忽略大小写
    text = 'This is some text -- with punctuation.'
    pattern = r'\bT\w+'
    with_case = re.compile(pattern)
    without_case = re.compile(pattern, re.IGNORECASE)

    print 'Input text               :', text
    print 'Pattern                  :', pattern

    print 'Case-sensitive:'
    for match in with_case.findall(text):
        print ' %r' % match
    print 'Case-insensitive:'
    for match in without_case.findall(text):
        print ' %r' % match
    print

def test_10():
    # 添加搜索选项--多行输入
    text = 'This is some text -- with punctuation.\nA second line.'
    pattern = r'(^\w+)|(\w+\S*$)'
    single_line = re.compile(pattern)
    multiline = re.compile(pattern, re.MULTILINE)

    print 'Input text               :', text
    print 'Pattern                  :', pattern

    print 'Single Line:'
    for match in single_line.findall(text):
        print ' %r' % (match, )
    print 'Multiline:'
    for match in multiline.findall(text):
        print ' %r' % (match, )
    print

def test_11():
    # 添加搜索选项--DOTALL，匹配除换行符之外的所有字符
    text = 'This is some text -- with punctuation.\nA second line.'
    pattern = r'.+'
    no_newlines = re.compile(pattern)
    dotall = re.compile(pattern, re.DOTALL)

    print 'Input text               :', text
    print 'Pattern                  :', pattern

    print 'no_newlines:'
    for match in no_newlines.findall(text):
        print ' %r' % (match, )
    print 'dotall:'
    for match in dotall.findall(text):
        print ' %r' % (match, )
    print

def test_12():
    import codecs
    import sys
    # 添加搜索选项--Unicode标志
    # 设置标志输出编码为UTF-8
    sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
    text = u'Fran中d z好人 中国人hao!'
    pattern = ur'\w+'
    ascii_pattern = re.compile(pattern)
    unicode_pattern = re.compile(pattern, re.UNICODE)
    print 'Input text               :', text
    print 'Pattern                  :', pattern
    print 'ASCII                    :', u', '.join(ascii_pattern.findall(text))
    print 'Unicode                  :', u', '.join(unicode_pattern.findall(text))

def test_13():
    address = re.compile('[\w\d.+-]+@([\w\d.]+\.)+(com|org|edu)', re.UNICODE)
    address = re.compile(
        '''
        [\w\d.+-]+      # username
        @
        ([\w\d.]+\.)+   # domain name prefix
        (com|org|edu)   # TODO: support more top-level domains
        ''',
        re.UNICODE | re.VERBOSE
    )
    address = re.compile(
        '''
        ((?P<name>
            ([\w.,]+\s+)*[\w.,]+)
            \s*
            <
        )?
        (?P<email>
            [\w\d.+-]+      # username
            @
            ([\w\d.]+\.)+   # domain name prefix
            (com|org|edu)   # TODO: support more top-level domains
        )
        >?
        ''',
        re.UNICODE | re.VERBOSE
    )
    candidates = [
        u'first.last@example.com',
        u'valid-address@mail.example.com',
        u'first.last+category@gmail.com',
        u'not-valid@example.foo',
        u'First Last <first.last@example.com>',
        u'No Brackets first.last@example.com',
        u'First Last',
        u'First Middle Last <first.last@example.com>',
        u'First M. Last <first.last@example.com>',
        u'<first.last@example.com>',
    ]
    for candidate in candidates:
        match = address.search(candidate)
        # print '%-35s %s' %(candidate, 'Matches' if match else 'No mathc')
        print ' Candidate   :', candidate
        if match:
            print ' Name    :', match.groupdict()['name']
            print ' Email   :', match.groupdict()['email']
        else:
            print ' No match'

def test_14():
    # 在模式中嵌入标志
    # IGNORECASE -- i  MULTILINE -- m  DOTALL -- s  UNICODE -- u  VERBOSE -- x
    text = 'This is some text -- with punctuation.'
    print 'Input text               :',text
    pattern = r'(?i)\bT\w+'
    regex = re.compile(pattern)
    match = regex.findall(text)
    print 'Pattern                  :', pattern
    print 'Matches                  :', match
    print

def test_15():
    # 向前断言(?=pattern)
    address = re.compile(
        '''
        ((?P<name>
            ([\w.,]+\s+)*[\w.,]+)
            \s+
        )
        (?= (<.*>$)
            |
            ([^<].*[^>]$)
        )
        <?

        (?P<email>
            [\w\d.+-]+      # username
            @
            ([\w\d.]+\.)+   # domain name prefix
            (com|org|edu)   # TODO: support more top-level domains
        )
        >?
        ''',
        re.UNICODE | re.VERBOSE
    )
    candidates = [
        u'First Last <first.last@example.com>',
        u'No Brackets first.last@example.com',
        u'Open Bracket <first.last@example.com',
        u'Close Bracket first.last@example.com>'
    ]
    for candidate in candidates:
        match = address.search(candidate)
        print ' Candidate   :', candidate
        if match:
            print ' Name    :', match.groupdict()['name']
            print ' Email   :', match.groupdict()['email']
        else:
            print ' No match'


def test_16():
    # 否定前向断言 （?!pattern）
    address = re.compile(
        '''
        ^
        (?!noreply@.*$)
        [\w\d.+-]+
        @
        ([\w\d.]+\.)+
        (com|org|edu)

        $
        ''',
        re.UNICODE | re.VERBOSE
    )
    candidates = [
        u'first.last@example.com',
        u'noreply@example.com'
    ]
    for candidate in candidates:
        match = address.search(candidate)
        print ' Candidate   :', candidate
        if match:
            print ' Match    :', candidate[match.start():match.end()]
        else:
            print ' No match'

def test_17():
    # 后向否定断言 （?<!pattern）
    address = re.compile(
        '''
        ^
        [\w\d.+-]+
        (?<!noreply)
        @
        ([\w\d.]+\.)+
        (com|org|edu)

        $
        ''',
        re.UNICODE | re.VERBOSE
    )
    candidates = [
        u'first.last@example.com',
        u'noreply@example.com'
    ]
    for candidate in candidates:
        match = address.search(candidate)
        print ' Candidate   :', candidate
        if match:
            print ' Match    :', candidate[match.start():match.end()]
        else:
            print ' No match'

def test_18():
    # 自引用表达式--数字
    address = re.compile(
        r'''
        (\w+)
        \s+
        (([\w.]+)\s+)?
        (\w+)

        \s+

        <

        (?P<email>
            \1
            \.
            \4
            @
            ([\w\d.]+\.)+
            (com|org|edu)
        )

        >
        ''',
        re.UNICODE | re.VERBOSE | re.IGNORECASE
    )
    candidates = [
        u'First Last <first.last@example.com>',
        u'Different Name <first.last@example.com>',
        u'First Middle Last <first.last@example>',
        u'First M. Last <first.last@example.com>',
    ]
    for candidate in candidates:
        match = address.search(candidate)
        print ' Candidate   :', candidate
        if match:
            print ' Match name    :', match.group(1), match.group(4)
            print ' Match email   :', match.group(5)
        else:
            print ' No match'

def test_19():
    # 自引用表达式--命名
    address = re.compile(
        r'''
        (?P<first_name>\w+)
        \s+
        (([\w.]+)\s+)?
        (?P<last_name>\w+)

        \s+

        <

        (?P<email>
            (?P=first_name)
            \.
            (?P=last_name)
            @
            ([\w\d.]+\.)+
            (com|org|edu)
        )

        >
        ''',
        re.UNICODE | re.VERBOSE | re.IGNORECASE
    )
    candidates = [
        u'First Last <first.last@example.com>',
        u'Different Name <first.last@example.com>',
        u'First Middle Last <first.last@example>',
        u'First M. Last <first.last@example.com>',
    ]
    for candidate in candidates:
        match = address.search(candidate)
        print ' Candidate   :', candidate
        if match:
            print ' Match name    :', match.groupdict()['first_name'], match.groupdict()['last_name']
            print ' Match email   :', match.groupdict()['email']
        else:
            print ' No match'


def test_20():
    # 查看组是否匹配
    address = re.compile(
        '''
        (?P<name>
            ([\w.,]+\s+)*[\w.,]+
        )?
        \s*
        (?(name)
            (?P<brackets>(?=(<.*>$)))
            |
            (?= ([^<].*[^>]$))
        )
        (?(brackets)<|\s*)

        (?P<email>
            [\w\d.+-]+      # username
            @
            ([\w\d.]+\.)+   # domain name prefix
            (com|org|edu)   # TODO: support more top-level domains
        )
        (?(brackets)>|\s*)
        ''',
        re.UNICODE | re.VERBOSE
    )
    candidates = [
        u'First Last <first.last@example.com>',
        u'<first.last@example.com>',
        u'No Brackets first.last@example.com',
        u'Open Bracket <first.last@example',
        u'Close Bracket first.last@example.com>',
        u'no.brackets@example.com',
    ]
    for candidate in candidates:
        match = address.search(candidate)
        print ' Candidate   :', candidate
        if match:
            print ' Match name    :', match.groupdict()['name']
            print ' Match email   :', match.groupdict()['email']
        else:
            print ' No match'

def test_21():
    # 用模式修改字符串
    # 用数字替换
    text = 'Make this **bold**.  This **too**.'
    bold = re.compile(r'\*{2}(.*?)\*{2}')

    print 'Text: ', text
    print 'Bold: ', bold.sub(r'<b>\1</b>', text)


    # 用命名组替换\g<name>
    bold = re.compile(r'\*{2}(?P<bold_text>.*?)\*{2}', re.UNICODE)
    print 'Text: ', text
    print 'Bold: ', bold.sub(r'<b>\g<bold_text></b>', text)

    # 限定替换次数
    bold = re.compile(r'\*{2}(.*?)\*{2}', re.UNICODE)
    print 'Text: ', text
    print 'Bold: ', bold.sub(r'<b>\1</b>', text, count=1)
    # subn与sub类似，只是会同时返回修改的字符串和完成的替换次数
    print 'Bold: ', bold.subn(r'<b>\1</b>', text)


def test_22():
    # 利用模式拆分
    text = '''
    on two lines.

    Paragraph two.


    Paragraph three.'''

    for num, para in enumerate(re.findall(r'(.+?)\n{2,}', text, flags=re.DOTALL)):
        print num, repr(para)
        print
    for num, para in enumerate(re.split(r'\n{2,}', text)):
        print num, repr(para)
        print
    for num, para in enumerate(re.split(r'(\n{2,})', text)):
        print num, repr(para)
        print

def test_23():
    filenames = ['../../test/pic.jpg', '.. a.jpg']
    for filename in filenames:
        print "filename: ",filename
        result = re.search(r'(.*)(?P<name>\w+\.(jpg|gif)$)', filename)
        if result:
            print "result: ", result.groupdict()['name']

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
    # test_11()
    # test_12()
    # test_13()
    # test_14()
    # test_15()
    # test_16()
    # test_17()
    # test_18()
    # test_19()
    # test_20()
    # test_21()
    # test_22()
    test_23()