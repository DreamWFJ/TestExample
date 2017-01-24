import logging
from cliff.show import ShowOne

class MyTest(ShowOne):
    "A simple test, maybe print your input args."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(MyTest, self).get_parser(prog_name)
        parser.add_argument('filename', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        filename = parsed_args.filename
        print type(filename)
        if filename:
            print "you input args : ", filename
        else:
            print "you input nothing"
        self.log.info("end test")
