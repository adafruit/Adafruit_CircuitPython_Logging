# SPDX-FileCopyrightText: 2024 Tim Cocks
# SPDX-License-Identifier: MIT


"""Briefly exercise the logger and null logger."""

import adafruit_logging as logging
# To test on CPython, un-comment below and comment out above
# import logging


logger = logging.getLogger("example")
logger.setLevel(logging.INFO)
print_handler = logging.StreamHandler()
logger.addHandler(print_handler)

default_formatter = logging.Formatter()
print_handler.setFormatter(default_formatter)
logger.info("Default formatter example")


timestamp_formatter = logging.Formatter(
    fmt="{asctime} {levelname}: {message}", style="{"
)
print_handler.setFormatter(timestamp_formatter)
logger.info("Timestamp formatter example")


custom_vals_formatter = logging.Formatter(
    fmt="{ip} {levelname}: {message}", style="{", defaults={"ip": "192.168.1.188"}
)
print_handler.setFormatter(custom_vals_formatter)
logger.info("Custom formatter example")
