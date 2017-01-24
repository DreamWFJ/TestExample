from debtcollector import removals
from debtcollector import renames
from debtcollector import moves
from debtcollector import updating
from debtcollector import deprecate
import warnings
warnings.simplefilter('always')
deprecate('This is no longer supported', version='1.0')
class Car(object):
    @removals.remove
    def start(self):
        print 'test'

    @moves.moved_method('meow')
    def mewow(self):
        return self.meow()
    def meow(self):
        return 'kitty'

c = Car()
print c.start()
print c.mewow()
print c.meow()

@removals.removed_class("Pinto")
class Pinto(object):
    pass

p = Pinto()

warnings.simplefilter('once')
class OldAndBusted(object):
    ip = '127.0.0.1'
    @removals.removed_kwarg('bleep')
    def __init__(self, bleep=None):
        self.bloop = bleep
    
    @updating.updated_kwarg_default_value('type', 'http', 'https')
    def url(self, type='http'):
        response = '%s://%s' %(type, self.ip)
        return response

    @classmethod
    @updating.updated_kwarg_default_value('type', 'http', 'https')
    def url(cls, type='http'):
        response = '%s://%s' %(type, cls.ip)
        return response
    @removals.remove
    @classmethod
    def fix_things(cls):
        pass
    
    @removals.removed_property
    def thing(self):
        return 'old-and-busted'

    @thing.setter
    def thing(self, value):
        pass

    @thing.deleter
    def thing(self):
        pass
    
    @removals.removed_kwarg('resp', message="Please use 'response' instead.")
    @classmethod
    def factory(cls, resp=None, response=None):
        response = resp or response
        return response

OldAndBusted.fix_things()
OldAndBusted.url()
OldAndBusted.factory(resp='super-duper')
o = OldAndBusted(bleep=2)
o.url()
o.thing
o.thing = '2'
del o.thing

def new_thing():
    return 'new thing'

old_thing = moves.moved_function(new_thing, 'old_thing', __name__)
print new_thing()
print old_thing()

class Dog(object):
    @property
    @moves.moved_property('bark')
    def burk(self):
        return self.bark
    @property
    def bark(self):
        return 'woof'

d = Dog()
print d.burk
print d.bark

class WizBang(object):
    pass
OldWizBang = moves.moved_class(WizBang, 'OldWizBang', __name__)    
a = OldWizBang()
b = WizBang

# removal_version = '?'
@renames.renamed_kwarg('snizzle', 'nizzle', message='Pretty please stop using it', version='0.5', removal_version='0.7')
def do_the_deed(snizzle=True, nizzle=True):
    return (snizzle, nizzle)
    
print do_the_deed()
print do_the_deed(snizzle=False)
print do_the_deed(nizzle=False)
