# -*- coding: utf-8 -*-
import sys
from cliff.app import App
from cliff.commandmanager import CommandManager


class DemoApp(App):
    # APP是首要继承的类
    def __init__(self):
        super(DemoApp, self).__init__(
            description='cliff demo app',
            version='0.1',
            command_manager=CommandManager('cliff.demo'),
            deferred_help=True,
            )
    # APP运行时首先初始化的东西，比如解析参数
    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')
    # 在执行命令之前的一些准备工作
    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)
    # 命令执行完成后的善后工作
    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = DemoApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))