#-*- coding:utf-8 -*-
from oslo_config import cfg
import sys
enable_apis_opt = cfg.ListOpt('enabled_apis',
				default=['ec2', 'osapi_compute'],
				help='List of APIs to enable by default.')

common_opts = [
	cfg.StrOpt('bind_host',
		default='0.0.0.0',
		help='IP address to list on.'),
	cfg.IntOpt('bind_port',
		default=9292,
		help='Port number to listen on.')
	]

rabbit_group = cfg.OptGroup(
	name='rabbit',
	title='RabbitMQ options'
	)

rabbit_ssl_opt = cfg.BoolOpt('use_ssl',
			default=False,
			help='use ssl for connection')

rabbit_Opts = [
	cfg.StrOpt('host',
		default='localhost',
		help='IP/hostname to listen on.'),
	cfg.IntOpt('port',
		default=5672,
		help='Port number to listen on.')
]

cli_opts = [  
    cfg.BoolOpt('verbose',  
                short='v',  
                default=False,  
                help='Print more verbose output.'),  
    cfg.BoolOpt('debug',  
                short='d',  
                default=False,  
                help='Print debugging output.'),  
]  

if __name__ == '__main__':
	CONF = cfg.ConfigOpts()

	CONF.register_opt(enable_apis_opt)
	CONF.register_opts(common_opts)
	CONF.register_group(rabbit_group)
	CONF.register_opts(rabbit_Opts, rabbit_group)
	# CONF.register_opts(rabbit_ssl_opt, rabbit_group)
	CONF.register_cli_opts(common_opts)
	CONF.register_cli_opts(cli_opts)
	CONF(args=sys.argv[1:], default_config_files=['my.conf'])
	# for i in CONF.enabled_apis:
	# 	print('DEFAULT.enabled_apis: ' + i)
	print "rabbit.host: " + CONF.rabbit.host
	print "common bind host: ",  CONF.bind_host
	print "cli opts : ", CONF.verbose, CONF.debug
	# print "Default.bind_port: " + CONF.bind_port
	# print "rabbit.use_ssl: " + str(CONF.rabbit.use_ssl)
	# print "rabbit.host: " + CONF.rabbit.host
	# print "rabbit.port: " + str(CONF.rabbit.port)
