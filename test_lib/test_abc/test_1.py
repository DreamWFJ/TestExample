import abc
class Sheep(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_size(self):
        return

class B(Sheep):
    def get_size(self):
        print 'abc'

a = B()
a.get_size()