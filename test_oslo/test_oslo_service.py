from oslo_config import cfg
from oslo_service import service

# CONF = cfg.CONF
# launcher = service.launch(CONF, service, workers=2)

# from foo.openstack.common import service
#
# launcher = service.launch(service, workers=2)


CONF = cfg.CONF

service_launcher = service.ServiceLauncher(CONF)
service_launcher.launch_service(service.Service())

process_launcher = service.ProcessLauncher(CONF, wait_interval=1.0)
process_launcher.launch_service(service.Service(), workers=2)