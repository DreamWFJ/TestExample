from _i18n import _, _LW, _LE
import logging as LOG
# ...

variable = "openstack"
LOG.warning(_LW('warning message: %s'), variable)


class AnException1(Exception):
    pass

class AnException2(Exception):
    pass

try:

    pass

except AnException1:

    # Log only
    LOG.exception(_LE('exception message'))

except AnException2:

    # Raise only
    raise RuntimeError(_('exception message'))

else:

    # Log and Raise
    msg = _('Unexpected error message')
    LOG.exception(msg)
    raise RuntimeError(msg)