# SPDX-FileCopyrightText: 2021 Alec Delaney for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`extensions`
====================================================

CircuitPython logging extension for logging to files

* Author(s): Alec Delaney
"""

from . import LoggingHandler


class FileHandler(LoggingHandler):
    """File handler for working with log files off of the microcontroller (like
    an SD card)

    :param filepath: The filepath to the log file
    :param mode: Whether to write ('w') or append ('a'); default is to append
    """

    def __init__(self, filepath: str, mode: str = "a"):
        self.logfile = open(filepath, mode, encoding="utf-8")

    def close(self):
        """Closes the file"""
        self.logfile.close()

    def format(self, level: int, msg: str):
        """Generate a string to log

        :param level: The level of the message
        :param msg: The message to format
        """
        return super().format(level, msg) + "\r\n"

    def emit(self, level: int, msg: str):
        """Generate the message and write it to the UART.

        :param level: The level of the message
        :param msg: The message to log
        """
        self.logfile.write(self.format(level, msg))
