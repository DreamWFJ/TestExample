from oslo_config import cfg
from oslo_log import log as logging
from oslo_i18n._i18n import _, _LI, _LW, _LE  # noqa

LOG = logging.getLogger(__name__)

def test_1():
    CONF = cfg.CONF
    DOMAIN = "demo"

    logging.register_options(CONF)
    # Optional step to set new defaults if necessary for
    # * logging_context_format_string
    # * default_log_levels

    extra_log_level_defaults = [
        'dogpile=INFO',
        'routes=INFO'
        ]

    logging.set_defaults(
        default_log_levels=logging.get_default_log_levels() +
        extra_log_level_defaults)

    logging.setup(CONF, DOMAIN)

    # Oslo Logging uses INFO as default
    LOG.info("Oslo Logging")
    LOG.warning("Oslo Logging")
    LOG.error("Oslo Logging")


if __name__ == '__main__':

    LOG.info(_LI("Welcome to Oslo Logging"))
    LOG.debug("A debugging message")  # Debug messages are not translated
    LOG.warning(_LW("A warning occurred"))
    LOG.error(_LE("An error occurred"))
    try:
        raise Exception(_("This is exceptional"))
    except Exception as err:
        LOG.error(err)