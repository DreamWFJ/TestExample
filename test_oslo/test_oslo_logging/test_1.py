from oslo_config import cfg
from oslo_context import context
from oslo_log import log as logging

CONF = cfg.CONF
DOMAIN = "demo"

logging.register_options(CONF)
CONF.logging_user_identity_format = "%(user)s/%(tenant)s@%(project_domain)s"
logging.setup(CONF, DOMAIN)

LOG = logging.getLogger(__name__)

LOG.info("Message without context")
# ids in Openstack are 32 characters long
# For readability a shorter id value is used
context.RequestContext(request_id='req-abc',
                       user='6ce90b4d',
                       tenant='d6134462',
                       project_domain='a6b9360e')
LOG.info("Message with context")


LOG.info("Message without context")
# ids in Openstack are 32 characters long
# For readability a shorter id value is used
context.RequestContext(user='6ce90b4d',
                       tenant='d6134462',
                       project_domain='a6b9360e')
LOG.info("=== Message with context")

context = context.RequestContext(user='ace90b4d',
                                 tenant='b6134462',
                                 project_domain='c6b9360e')
LOG.info("Message with passed context", context=context)

