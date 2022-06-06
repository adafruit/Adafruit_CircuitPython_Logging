# SPDX-FileCopyrightText: 2019 Dave Astels for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_logging`
================================================================================

Logging module for CircuitPython


* Author(s): Dave Astels

Implementation Notes
--------------------

**Hardware:**


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

Attributes
----------
    LEVELS : list
        A list of tuples representing the valid logging levels used by
        this module. Each tuple contains exactly two elements: one int and one
        str. The int in each tuple represents the relative severity of that
        level (00 to 50). The str in each tuple is the string representation of
        that logging level ("NOTSET" to "CRITICAL"; see below).
    NOTSET : int
        The NOTSET logging level, which is a dummy logging level that can be
        used to indicate that a `Logger` should not print any logging messages,
        regardless of how severe those messages might be (including CRITICAL).
    DEBUG : int
        The DEBUG logging level, which is the lowest (least severe) real level.
    INFO : int
        The INFO logging level for informative/informational messages.
    WARNING : int
       The WARNING logging level for warnings that should be addressed/fixed.
    ERROR : int
        The ERROR logging level for Python exceptions that occur during runtime.
    CRITICAL : int
        The CRITICAL logging level, which is the highest (most severe) level for
        unrecoverable errors that have caused the code to halt and exit.

"""
# pylint:disable=redefined-outer-name,consider-using-enumerate,no-self-use
# pylint:disable=invalid-name

import time
import sys

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Logger.git"
# pylint:disable=undefined-all-variable
__all__ = [
    "LEVELS",
    "NOTSET",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "_level_for",
    "Handler",
    "StreamHandler",
    "logger_cache",
    "getLogger",
    "Logger",
    "NullHandler",
    "FileHandler",
]


LEVELS = [
    (00, "NOTSET"),
    (10, "DEBUG"),
    (20, "INFO"),
    (30, "WARNING"),
    (40, "ERROR"),
    (50, "CRITICAL"),
]

for __value, __name in LEVELS:
    globals()[__name] = __value


def _level_for(value: int) -> str:
    """Convert a numeric level to the most appropriate name.

    :param int value: a numeric level

    """
    for i in range(len(LEVELS)):
        if value == LEVELS[i][0]:
            return LEVELS[i][1]
        if value < LEVELS[i][0]:
            return LEVELS[i - 1][1]
    return LEVELS[0][1]


#  pylint: disable=too-few-public-methods
class Handler:
    """Abstract logging message handler."""

    def __init__(self, level=NOTSET):  # pylint: disable=undefined-variable
        self.level = level
        """Level of the handler; this is currently unused, and
        only the level of the logger is used"""

    def _format(self, log_level: int, message: str) -> str:
        """Generate a timestamped message.

        :param int log_level: the logging level
        :param str message: the message to log

        """
        return "{0:<0.3f}: {1} - {2}".format(
            time.monotonic(), _level_for(log_level), message
        )

    def _emit(self, log_level: int, message: str):
        """Send a message where it should go.
        Placeholder for subclass implementations.
        """
        raise NotImplementedError()


#  pylint: disable=too-few-public-methods
class StreamHandler(Handler):
    """Send logging messages to a stream, `sys.stderr` (typically
    the serial console) by default.

    :param stream: The stream to log to, default is `sys.stderr`
    """

    def __init__(self, stream=None):
        super().__init__()
        if stream is None:
            stream = sys.stderr
        self.stream = stream
        """The stream to log to"""

    def _emit(self, log_level: int, message: str):
        """Send a message to the console.

        :param int log_level: the logging level
        :param str message: the message to log

        """
        print(self._format(log_level, message))


# The level module-global variables get created when loaded
# pylint:disable=undefined-variable

logger_cache = {}


def _addLogger(logger_name: str):
    """Adds the logger if it doesn't already exist"""
    if logger_name not in logger_cache:
        logger_cache[logger_name] = Logger(logger_name)


# pylint:disable=global-statement
def getLogger(logger_name: str) -> "Logger":
    """Create or retrieve a logger by name; only retrieves loggers
    made using this function; if a Logger with this name does not
    exist it is created

    :param str logger_name: The name of the `Logger` to create/retrieve.

    """
    _addLogger(logger_name)
    return logger_cache[logger_name]


# pylint:enable=global-statement


class Logger:
    """Provide a logging api."""

    def __init__(self, name: str, level=NOTSET):
        """Create an instance."""
        self._level = level
        self.name = name
        """The name of the logger, this should be unique for proper
        functionality of `getLogger()`"""
        self._handler = None

    def setLevel(self, log_level: int):
        """Set the logging cutoff level.

        :param int log_level: the lowest level to output

        """
        self._level = log_level

    def getEffectiveLevel(self) -> int:
        """Get the effective level for this logger.

        :return: the lowest level to output

        """
        return self._level

    def addHandler(self, hdlr: Handler):
        """Sets the handler of this logger to the specified handler.

        *NOTE* this is slightly different from the CPython equivalent which adds
        the handler rather than replacing it.

        :param Handler hdlr: the handler

        """
        self._handler = hdlr

    def hasHandlers(self) -> bool:
        """Whether any handlers have been set for this logger"""
        return self._handler is not None

    def log(self, level: int, msg: str, *args):
        """Log a message.

        :param int level: the priority level at which to log
        :param str msg: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        if self._handler and level >= self._level:
            self._handler._emit(level, msg % args)  #  pylint: disable=protected-access

    def debug(self, msg: str, *args):
        """Log a debug message.

        :param str fmsg: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        self.log(DEBUG, msg, *args)

    def info(self, msg: str, *args):
        """Log a info message.

        :param str msg: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        self.log(INFO, msg, *args)

    def warning(self, msg: str, *args):
        """Log a warning message.

        :param str msg: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        self.log(WARNING, msg, *args)

    def error(self, msg: str, *args):
        """Log a error message.

        :param str msg: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        self.log(ERROR, msg, *args)

    def critical(self, msg: str, *args):
        """Log a critical message.

        :param str msg: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        self.log(CRITICAL, msg, *args)


class NullHandler(Handler):
    """Provide an empty log handler.

    This can be used in place of a real log handler to more efficiently disable
    logging."""

    def setLevel(self, log_level: int):
        """Dummy implementation."""

    def getEffectiveLevel(self) -> int:
        """Dummy implementation."""
        return NOTSET

    def addHandler(self, handler: Handler):
        """Dummy implementation."""

    def log(self, log_level: int, format_string: str, *args):
        """Dummy implementation."""

    def debug(self, msg: str, *args):
        """Dummy implementation."""

    def info(self, msg: str, *args):
        """Dummy implementation."""

    def warning(self, msg: str, *args):
        """Dummy implementation."""

    def error(self, msg: str, *args):
        """Dummy implementation."""

    def critical(self, msg: str, *args):
        """Dummy implementation."""

    def _emit(self, log_level: int, message: str):
        """Dummy implementation"""


class FileHandler(StreamHandler):
    """File handler for working with log files off of the microcontroller (like
    an SD card)

    :param str filename: The filename of the log file
    :param str mode: Whether to write ('w') or append ('a'); default is to append
    """

    def __init__(self, filename: str, mode: str = "a") -> None:
        # pylint: disable=consider-using-with
        super().__init__(open(filename, mode=mode))

    def close(self):
        """Closes the file"""
        self.stream.close()

    def _format(self, log_level: int, message: str):
        """Generate a string to log

        :param level: The level of the message
        :param msg: The message to format
        """
        return super()._format(log_level, message) + "\r\n"

    def _emit(self, log_level: int, message: str):
        """Generate the message and write it to the UART.

        :param level: The level of the message
        :param msg: The message to log
        """
        self.stream.write(self._format(log_level, message))
