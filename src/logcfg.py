'''
    Set up and configure logging, custom levels, and filtering.

    TODO: configure mail with:
          http://flask.pocoo.org/docs/0.12/errorhandling/#error-mails
'''
import sys
import traceback
import logging, logging.handlers
from logging import Formatter

from .main import app

DEBUG_TEMPL = '  %(levelname)-7.7s %(funcName)s: %(message)s'
PROD_TEMPL  = '%(asctime)s %(levelname)-7.7s %(funcName)s: %(message)s'

# new level constants
logging.NOTE = 32       # positive yet important, above default filter
logging.EXCEPT = 42     # app exception
DEBUG = logging.DEBUG

log = logging.getLogger()
Formatter_format = Formatter.format  # shortcut


# logging classes
class ColorFmtr(Formatter):
    ''' Colors the levelname of a log message. '''
    def __init__(self, *args, **kwargs):
        Formatter.__init__(self, *args, **kwargs)
        white_on_red = b'\x1b[37;1;41m'
        self.colormap = colormap = dict(
            DEBUG    = b'\x1b[34m',                  # blue
            INFO     = b'\x1b[32m',                  # green
            WARNING  = b'\x1b[33;1m',                # yellow bold
            NOTE     = b'\x1b[36;1m',                # cyan bold
            ERROR    = b'\x1b[31;1m',                # red bold
            EXCEPT   = b'\x1b[31;1m',                # red bold
            CRITICAL = white_on_red,
            FATAL    = white_on_red,
            NOTSET   = b'\x1b[0m',                   # reset
        )
        self.icomap = icomap = dict(
            DEBUG       = '•',
            INFO        = '✓',
            WARNING     = '⚠',
            NOTE        = '★',
            ERROR       = '✗',
            EXCEPT      = '💣',
            CRITICAL    = '💀',
            FATAL       = '💀',
            NOTSET      = '•',
        )
        # "render" levels
        for levelname in colormap.keys():
            if levelname == 'NOTSET':
                continue
            colormap[levelname] = '%s%s %s%s' % (
                colormap.get(levelname, '').decode('ascii'),  # to str
                icomap[levelname],
                levelname,
                colormap['NOTSET'].decode('ascii'),  # to str
            )

    def format(self, record):
        ''' Log color formatting, probably could be done better. '''
        levelname = record.levelname
        s = Formatter_format(self, record)
        s = s.replace(levelname, self.colormap.get(levelname, levelname), 1)
        return s


def makefunc(level):
    ''' A convenience function for adding to a Logger. '''
    if level == logging.EXCEPT:
        # if an exception and debug level, emit the traceback
        def tb_func(msg, *args, **kwargs):
            log._log(level, msg, args, **kwargs)
            if log.isEnabledFor(logging.DEBUG):
                log.debug(traceback.format_exc())
        return tb_func

    def thefunc(msg, *args, **kwargs):
        if log.isEnabledFor(level):
            log._log(level, msg, args, **kwargs)

    return thefunc


# set up logging, custom levels
logging.addLevelName(logging.NOTE, 'NOTE')          # new levels
logging.addLevelName(logging.EXCEPT, 'EXCEPT')
logging.addLevelName(logging.CRITICAL, 'FATAL')     # copy critical to fatal

# add convenience funcs
log.note    = makefunc(logging.NOTE)
log.exc     = makefunc(logging.EXCEPT)

console_log = logging.StreamHandler(sys.stdout)
if app.debug:
    console_level = logging.DEBUG
    console_log.setFormatter(ColorFmtr(DEBUG_TEMPL))
    # third party:
    #~ logging.getLogger('sqlalchemy.engine').setLevel(console_level)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)  # D too much
else:
    console_level = logging.INFO
    console_log.setFormatter(Formatter(PROD_TEMPL))

log.addHandler(console_log)
log.setLevel(console_level)
