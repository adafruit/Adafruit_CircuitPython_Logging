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
    "level_for",
    "LoggingHandler",
    "PrintHandler",
    "logger_cache",
    "null_logger",
    "getLogger",
    "Logger",
    "NullLogger",
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


def level_for(value: int) -> str:
    """Convert a numeric level to the most appropriate name.

    :param int value: a numeric level

    """
    for i in range(len(LEVELS)):
        if value == LEVELS[i][0]:
            return LEVELS[i][1]
        if value < LEVELS[i][0]:
            return LEVELS[i - 1][1]
    return LEVELS[0][1]


class LoggingHandler:
    """Abstract logging message handler."""

    def format(self, log_level: int, message: str) -> str:
        """Generate a timestamped message.

        :param int log_level: the logging level
        :param str message: the message to log

        """
        return "{0:<0.3f}: {1} - {2}".format(
            time.monotonic(), level_for(log_level), message
        )

    def emit(self, log_level: int, message: str):
        """Send a message where it should go.
        Placeholder for subclass implementations.
        """
        raise NotImplementedError()


class PrintHandler(LoggingHandler):
    """Send logging messages to the console by using print."""

    def emit(self, log_level: int, message: str):
        """Send a message to the console.

        :param int log_level: the logging level
        :param str message: the message to log

        """
        print(self.format(log_level, message))


# The level module-global variables get created when loaded
# pylint:disable=undefined-variable

logger_cache = {}
null_logger = None

# pylint:disable=global-statement
def getLogger(logger_name: str) -> "Logger":
    """Create or retrieve a logger by name.

    :param str logger_name: The name of the `Logger` to create/retrieve. `None`
                            will cause the `NullLogger` instance to be returned.

    """
    global null_logger
    if not logger_name or logger_name == "":
        if not null_logger:
            null_logger = NullLogger()
        return null_logger

    if logger_name not in logger_cache:
        logger_cache[logger_name] = Logger()
    return logger_cache[logger_name]


# pylint:enable=global-statement


class Logger:
    """Provide a logging api."""

    def __init__(self):
        """Create an instance."""
        self._level = NOTSET
        self._handler = PrintHandler()

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

    def addHandler(self, handler: LoggingHandler):
        """Sets the handler of this logger to the specified handler.
        *NOTE* this is slightly different from the CPython equivalent which adds
        the handler rather than replacing it.

        :param LoggingHandler handler: the handler

        """
        self._handler = handler

    def log(self, log_level: int, format_string: str, *args):
        """Log a message.

        :param int log_level: the priority level at which to log
        :param str format_string: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        if log_level >= self._level:
            self._handler.emit(log_level, format_string % args)

    def debug(self, format_string: str, *args):
        """Log a debug message.

        :param str format_string: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        self.log(DEBUG, format_string, *args)

    def info(self, format_string: str, *args):
        """Log a info message.

        :param str format_string: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        self.log(INFO, format_string, *args)

    def warning(self, format_string: str, *args):
        """Log a warning message.

        :param str format_string: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        self.log(WARNING, format_string, *args)

    def error(self, format_string: str, *args):
        """Log a error message.

        :param str format_string: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        self.log(ERROR, format_string, *args)

    def critical(self, format_string: str, *args):
        """Log a critical message.

        :param str format_string: the core message string with embedded
                                  formatting directives
        :param args: arguments to ``format_string.format()``; can be empty

        """
        self.log(CRITICAL, format_string, *args)


class NullLogger:
    """Provide an empty logger.
    This can be used in place of a real logger to more efficiently disable
    logging."""

    def __init__(self):
        """Dummy implementation."""

    def setLevel(self, log_level: int):
        """Dummy implementation."""

    def getEffectiveLevel(self) -> int:
        """Dummy implementation."""
        return NOTSET

    def addHandler(self, handler: LoggingHandler):
        """Dummy implementation."""

    def log(self, log_level: int, format_string: str, *args):
        """Dummy implementation."""

    def debug(self, format_string: str, *args):
        """Dummy implementation."""

    def info(self, format_string: str, *args):
        """Dummy implementation."""

    def warning(self, format_string: str, *args):
        """Dummy implementation."""

    def error(self, format_string: str, *args):
        """Dummy implementation."""

    def critical(self, format_string: str, *args):
        """Dummy implementation."""
