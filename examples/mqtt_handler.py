# SPDX-FileCopyrightText: 2022 vladak
# SPDX-License-Identifier: Unlicense
"""
MQTT logging handler - log records will be published as MQTT messages
"""

import adafruit_minimqtt.adafruit_minimqtt as MQTT

# adafruit_logging defines log levels dynamically.
# pylint: disable=no-name-in-module
from adafruit_logging import NOTSET, Handler, LogRecord


class MQTTHandler(Handler):
    """
    Log handler that emits log records as MQTT PUBLISH messages.
    """

    def __init__(self, mqtt_client: MQTT.MQTT, topic: str) -> None:
        """
        Assumes that the MQTT client object is already connected.
        """
        super().__init__()

        self._mqtt_client = mqtt_client
        self._topic = topic

        # To make it work also in CPython.
        self.level = NOTSET

    def emit(self, record: LogRecord) -> None:
        """
        Publish message from the LogRecord to the MQTT broker, if connected.
        """
        try:
            if self._mqtt_client.is_connected():
                self._mqtt_client.publish(self._topic, record.msg)
        except MQTT.MMQTTException:
            pass

    # To make this work also in CPython's logging.
    def handle(self, record: LogRecord) -> None:
        """
        Handle the log record. Here, it means just emit.
        """
        self.emit(record)
