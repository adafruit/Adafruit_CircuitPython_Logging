# SPDX-FileCopyrightText: 2021 Alec Delaney
# SPDX-License-Identifier: MIT

import board
import sdcardio
import storage
import adafruit_logging as logging

# Initialize SD card
spi = board.SPI()
sdcard = sdcardio.SDCard(spi, board.D10)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, '/sd')

# Initialize log functionality
log_filepath = "/sd/testlog.log"
logger = logging.getLogger("testlog")
file_handler = logging.FileHandler(log_filepath)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger.info("Logger initialized!")
logger.debug("You can even add debug statements to the log!")