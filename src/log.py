import logging
import logging.config
import os


def create_logger():
    """The logger constructor, called by every Pipe at initation.

    Retuns:
        logging.Logger

    """

    logname = 'reporting'
    logdir = os.path.join(os.getcwd(), 'log')

    # Create log folder if it does not exist
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    # Logger config
    config = {
        'disable_existing_loggers': False,
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(module)s - %(levelname)s - %(message)s'
            },
            'json': {
                'format': '{"TS":"%(asctime)s","MOD":"%(module)s","LVL":"%(levelname)s","MSG":"%(message)s"}'
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'formatter': 'default',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'DEBUG',
                'formatter': 'json',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(logdir, logname + '.log')
            }
        },
        'loggers': {
            logname: {
                'handlers': ['console', 'file'],
                'level': 'DEBUG'
            },
        },
    }

    # Set logging config
    logging.config.dictConfig(config)
    logger = logging.getLogger(logname)

    return logger
