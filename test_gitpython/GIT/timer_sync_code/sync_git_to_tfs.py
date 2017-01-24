# -*- coding: utf-8 -*-
import logging
import logging.handlers
from apscheduler.schedulers.blocking import BlockingScheduler
import os
current_path = os.getcwd()



LOG_FILENAME = 'sync_git.log'
logger = logging.getLogger('sync_git_to_tfs')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)
rh = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=4*1024, backupCount=100
)
rh.setFormatter(formatter)
logger.addHandler(rh)

def excute_shell():
	"""
	"""
	logger.info("starting call shell script, sync git code to tfs")
	os.chdir(current_path)
	shell_script_name = "%s/%s"%(current_path, "sync_code.sh")
	os.system("bash %s"%shell_script_name)
	logger.info("finished execute shell script, wait the next time")


def main():
	logger.info("starting time sync task")
	scheduler = BlockingScheduler()
	scheduler.add_job(excute_shell, 'cron', hour='1')
	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit), e:
		logger.warning("catch a exception, and exit")
		scheduler.shutdown()
	logger.info("stopping time sync task")

if __name__ == '__main__':
	main()