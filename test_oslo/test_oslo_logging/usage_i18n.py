"""A usage example of Oslo Logging with Oslo i18n

This example requires the following package to be installed.
$ pip install oslo.log

Additional Oslo packages installed include oslo.config, oslo.context,
oslo.i18n, osli.serialization and oslo.utils.

More information about Oslo Logging can be found at:

  http://docs.openstack.org/developer/oslo.log/usage.html
  http://docs.openstack.org/developer/oslo.i18n/usage.html
"""

from oslo_config import cfg
from oslo_log import log as logging
from _i18n import _, _LI, _LW, _LE  # noqa

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = 'demo'


def prepare():
    """Prepare Oslo Logging (2 or 3 steps)

    Use of Oslo Logging involves the following:

    * logging.register_options
    * logging.set_defaults (optional)
    * logging.setup
    """

    # Required step to register common, logging and generic configuration
    # variables
    logging.register_options(CONF)

    # Optional step to set new defaults if necessary for
    # * logging_context_format_string
    # * default_log_levels
    #
    # These variables default to respectively:
    #
    #  import oslo_log
    #  oslo_log._options.DEFAULT_LOG_LEVELS
    #  oslo_log._options.log_opts[0].default
    #

    extra_log_level_defaults = [
        'dogpile=INFO',
        'routes=INFO'
        ]

    logging.set_defaults(
        default_log_levels=logging.get_default_log_levels() +
        extra_log_level_defaults)

    # Required setup based on configuration and domain
    logging.setup(CONF, DOMAIN)


if __name__ == '__main__':
    prepare()
    # NOTE: These examples use Oslo i18n marker functions

    LOG.info(_LI("Welcome to Oslo Logging"))
    LOG.debug("A debugging message")  # Debug messages are not translated
    LOG.warning(_LW("A warning occurred"))
    LOG.error(_LE("An error occurred"))
    try:
        raise Exception(_("This is exceptional"))
    except Exception:
        LOG.exception(_LE("An Exception occurred"))