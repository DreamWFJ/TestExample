import glob
import logging
import logging.handlers

LOG_FILENAME = 'logging_rotatingfile_example.out'
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=20, backupCount=3
)
my_logger.addHandler(handler)

for i in range(20):
    my_logger.debug('i = %d'%i)

logfiles = glob.glob('%s*'%LOG_FILENAME)
for filename in logfiles:
    print filename