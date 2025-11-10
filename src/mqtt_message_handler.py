from .server import Server
from .modbus_mqtt import MqttClient
import logging
logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self, servers: list[Server], mqtt_client: MqttClient):
        self.devices = servers
        self.mqtt_client = mqtt_client

    def _decode_subscribed_topic(self, msg_topic: str) -> tuple[Server, str]:
        """
            Finds the implicated device and its register, by MQTT message topic.

        Args:
            msg_topic (str): topic of the incoming message (usually a command_topic)

        Raises:
            ValueError: If the command_topic format does not match any of the defined devices

        Returns:
            tuple[str, str]: _description_
        """
        # command_topic = f"{self.base_topic}/{server.nickname}/{slugify(register_name)}/set"
        logger.info(f"decoding {msg_topic}")
        server_ha_display_name: str = msg_topic.split('/')[1]
        s = None
        for s in self.devices: 
            logger.info(f"comparing {s.name}, {server_ha_display_name}")
            if s.name.lower() == server_ha_display_name:
                device = s
                break
        if device is None: raise ValueError(f"Server {server_ha_display_name} not available. Cannot write.")
        register_name: str = msg_topic.split('/')[2]

        logger.info(f"Decoded {msg_topic=}: {device=}, {register_name=}")
        return (device, register_name)

    def decode_and_write(self, msg_topic: str, msg_payload_decoded: str) -> None:
        """
            Finds implied register from topic, writes and updates entity state by a read back.
        """
        # find implied register from topic
        server, register_name = self._decode_subscribed_topic(msg_topic)

        # write
        server.write_registers(register_name, msg_payload_decoded)

        # update state by read back
        value = server.read_registers(server.write_parameters_slug_to_name[register_name])
        logger.info(f"Read back after write attempt {value=}")
        self.mqtt_client.publish_to_ha(
            register_name, value, server)
    