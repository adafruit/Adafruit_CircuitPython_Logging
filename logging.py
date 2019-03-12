# The MIT License (MIT)
#
# Copyright (c) 2019 Dave Astels for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`logging`
================================================================================

Logging module for CircuitPython


* Author(s): Dave Astels

Implementation Notes
--------------------

**Hardware:**


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""
#pylint:disable=redefined-outer-name,consider-using-enumerate,no-self-use

import time

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Logger.git"


LEVELS = [(00, 'NOTSET'),
          (10, 'DEBUG'),
          (20, 'INFO'),
          (30, 'WARNING'),
          (40, 'ERROR'),
          (50, 'CRITICAL')]

for value, name in LEVELS:
    globals()[name] = value

def level_for(value):
    """Convert a numberic level to the most appropriate name.

    :param value: a numeric level

    """
    for i in range(len(LEVELS)):
        if value == LEVELS[i][0]:
            return LEVELS[i][1]
        elif value < LEVELS[i][0]:
            return LEVELS[i-1][1]
    return LEVELS[0][1]

class LoggingHandler(object):
    """Abstract logging message handler."""

    def format(self, level, msg):
        """Generate a timestamped message.

        :param level: the logging level
        :param msg: the message to log

        """
        now = time.localtime()
        time_vals = (now.tm_year, now.tm_mon, now.tm_mday,
                     now.tm_hour, now.tm_min, now.tm_sec)
        timestamp = '%4d/%02d/%02d %02d:%02d:%02d' % time_vals
        return '{0}: {1} - {2}'.format(timestamp, level_for(level), msg)

    def emit(self, level, msg):
        """Send a message where it should go.
        Place holder for subclass implementations.
        """
        raise NotImplementedError()


class PrintHandler(LoggingHandler):
    """Send logging messages to the console by using print."""

    def emit(self, level, msg):
        """Send a message to teh console.

        :param level: the logging level
        :param msg: the message to log

        """
        print(self.format(level, msg))


# The level module-global variables get created when loaded
#pylint:disable=undefined-variable

logger_cache = dict()

def getLogger(name):
    if name not in logger_cache:
        logger_cache[name] = Logger()
    return logger_cache[name]

class Logger(object):
    """Provide a logging api."""

    def __init__(self, handler=None):
        """Create an instance.

        :param handler: what to use to output messages. Defaults to a PrintHandler.

        """
        self._level = NOTSET
        if handler is None:
            self._handler = PrintHandler()
        else:
            self._handler = handler

    def setLevel(self, value):
        self._level = value

    def log(self, level, format_string, *args):
        """Log a message.

        :param level: the priority level at which to log
        :param format_string: the core message string with embedded formatting directives
        :param args: arguments to ``format_string.format()``, can be empty

        """
        if level >= self._level:
            self._handler.emit(level, format_string % args)

    def debug(self, format_string, *args):
        """Log a debug message.

        :param format_string: the core message string with embedded formatting directives
        :param args: arguments to ``format_string.format()``, can be empty

        """
        self.log(DEBUG, format_string, *args)

    def info(self, format_string, *args):
        """Log a info message.

        :param format_string: the core message string with embedded formatting directives
        :param args: arguments to ``format_string.format()``, can be empty

        """
        self.log(INFO, format_string, *args)

    def warning(self, format_string, *args):
        """Log a warning message.

        :param format_string: the core message string with embedded formatting directives
        :param args: arguments to ``format_string.format()``, can be empty

        """
        self.log(WARNING, format_string, *args)

    def error(self, format_string, *args):
        """Log a error message.

        :param format_string: the core message string with embedded formatting directives
        :param args: arguments to ``format_string.format()``, can be empty

        """
        self.log(ERROR, format_string, *args)

    def critical(self, format_string, *args):
        """Log a critical message.

        :param format_string: the core message string with embedded formatting directives
        :param args: arguments to ``format_string.format()``, can be empty

        """
        self.log(CRITICAL, format_string, *args)
