"""
Demonstrate how to use a single logger to emit log records to
both console and MQTT broker, in this case Adafruit IO.
"""

import json
import socket
import ssl

import adafruit_minimqtt.adafruit_minimqtt as MQTT
from mqtt_handler import MQTTHandler

import adafruit_logging as logging

logger = logging.getLogger(__name__)

broker = "io.adafruit.com"
port = 8883
username = "Adafruit_IO_username"
password = "Adafruit_IO_key"
feedname = "Adafruit_feed_name"
mqtt_topic = f"{username}/feeds/{feedname}"
mqtt_client = MQTT.MQTT(
    broker=broker,
    port=port,
    username=username,
    password=password,
    socket_pool=socket,
    ssl_context=ssl.create_default_context(),
)
mqtt_client.connect()
mqtt_handler = MQTTHandler(mqtt_client, mqtt_topic)
print("adding MQTT handler")
logger.addHandler(mqtt_handler)

stream_handler = logging.StreamHandler()
print("adding Stream handler")
logger.addHandler(stream_handler)

data = "foo bar"
print("logging begins !")
# This should emit both to the console as well as to the MQTT broker.
logger.warning(json.dumps(data))
