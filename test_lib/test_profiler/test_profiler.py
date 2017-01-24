# -*- coding: utf-8 -*-
from osprofiler import profiler
from osprofiler import notifier
import json

def test_1():
    # 使用前，一定要init，否则不会用任何的数据记录
    profiler.init("SECRET_HMAC_KEY", base_id='sadfsdafasdfasdfas', parent_id='dsafafasdfsadf')

    def some_func():
        profiler.start("point_name", {"any_key": "with_any_value"})
        # your code
        profiler.stop({"any_info_about_point": "in_this_dict"})


    @profiler.trace("point_name",
                    info={"any_info_about_point": "in_this_dict"},
                    hide_args=False)
    def some_func2(*args, **kwargs):
        # If you need to hide args in profile info, put hide_args=True
        pass

    def some_func3():
        with profiler.Trace("point_name",
                            info={"any_key": "with_any_value"}):
            pass

    @profiler.trace_cls("point_name", info={}, hide_args=False,
                        trace_private=False)
    class TracedClass(object):

        def traced_method(self):
            print "test--------"

        def _traced_only_if_trace_private_true(self):
             pass

    # 把所有的记录写入到json文件里面
    def send_info_to_file_collector(info, context=None):
        with open("traces", "a") as f:
            f.write(json.dumps(info))

    notifier.set(send_info_to_file_collector)
    # 下面的函数调用都会被一一记录
    some_func()
    some_func2(test='asdfasdf', adf=313)


    trace = TracedClass()
    trace.traced_method()

import cProfile
import re
def test_2():
    cProfile.run('re.compile("foo|bar")')

if __name__ == '__main__':
    # test_2()
    pass