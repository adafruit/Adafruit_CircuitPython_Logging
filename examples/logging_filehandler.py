# SPDX-FileCopyrightText: 2021 Alec Delaney
# SPDX-License-Identifier: MIT

import adafruit_logging as logging

# Initialize log functionality on a writable medium, like an SD card
log_filepath = "/sd/testlog.log"
logger = logging.getLogger("testlog")
file_handler = logging.FileHandler(log_filepath)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger.info("Logger initialized!")
logger.debug("You can even add debug statements to the log!")
