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
`adafruit_logger`
================================================================================

UART message handler for the Logging module for CircuitPython


* Author(s): Dave Astels

Implementation Notes
--------------------

**Hardware:**


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""
#pylint:disable=missing-super-argument

# Example:
#
# import board
# import busio
# from adafruit_logger.uart_handler import UartHandler
# from adafruit_logger import *
#
# uart = busio.UART(board.TX, board.RX, baudrate=115200)
# logger = Logger(UartHandler(uart))
# logger.level = INFO
# logger.info('testing')

from adafruit_logger import LoggingHandler

class UartHandler(LoggingHandler):

    def __init__(self, uart):
        self._uart = uart

    def format(self, level, msg):
        return super().format(level, msg) + '\r\n'

    def emit(self, level, msg):
        self._uart.write(bytes(self.format(level, msg), 'utf-8'))
