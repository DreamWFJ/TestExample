from oslo_cache import core
from oslo_config import cfg
import oslo_cache

conf = cfg.CONF
NO_VALUE = core.NO_VALUE

MEMOIZE = oslo_cache.core.get_memoization_decorator(conf,
                                                    group='group1')

@MEMOIZE
def function(arg1, arg2):
    pass


ALTERNATE_MEMOIZE = oslo_cache.core.get_memoization_decorator(
    conf, group='group2', expiration_group='group3')

@ALTERNATE_MEMOIZE
def function2(arg1, arg2):
    pass

