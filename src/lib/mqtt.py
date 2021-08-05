import gc
from umqtt.robust2 import MQTTClient
from ubinascii import hexlify
from machine import unique_id
gc.collect()

class atMQTTClient(MQTTClient):

    def __init__(self, mqttconfig) -> None:
        # MQTT config
        self._client_id = hexlify(unique_id())
        self._user = mqttconfig['user']
        self._pswd = mqttconfig['mqtt_pw']
        self._ssl = mqttconfig['ssl']
        self._ssl_params = mqttconfig['ssl_params']
        # Callbacks and coros
        #self._cb = callback
        #self._wifi_handler = wifi_han
        #self._connect_handler = conn_han
        # Network
        self._port = mqttconfig['port']
        if self._port == 0:
            self._port = 8883 if self._ssl else 1883
        self._server = mqttconfig['server']
        if self._server is None:
            raise ValueError('no server specified.')
        self._sock = None
        super().__init__(self._client_id, self._server,self._port,self._pswd,)


        MQTTClient(client_id, server, port=0, user=None, password=None, keepalive=0, ssl=False, ssl_params={})
