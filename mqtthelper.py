import logging
import paho.mqtt.publish
from abc import ABC, abstractmethod


class MqttHelper(ABC):

    def __init__(self):
        self.logger = logging.getLogger()

    @abstractmethod
    def theme(self, theme: str) -> None:
        '''
        Display the relevant theme on the LED matrix display
        '''
        pass

    @abstractmethod
    def off(self) -> None:
        '''
        Switch the LED matrix off
        '''
        pass


class RealMqttHelper(MqttHelper):

    def __init__(self, host: str):
        super().__init__()
        self.host = host

    def theme(self, theme: str):
        try:
            self.logger.info(f"sending led-display/theme:{theme} to {self.host}")
            paho.mqtt.publish.single('led-display/theme', theme, hostname=self.host)
        except:
            self.logger.error('failed to publish led-display/theme message')

    def off(self):
        try:
            self.logger.info(f"sending led-display/off to {self.host}")
            paho.mqtt.publish.single('led-display/off', hostname=self.host)
        except:
            self.logger.error('failed to publish led-display/off message')


class FakeMqttHelper(MqttHelper):

    def __init__(self):
        super().__init__()

    def theme(self, theme: str) -> None:
        self.logger.debug(f'set theme to {theme}')

    def off(self) -> None:
        self.logger.debug('switch display off')


def get(enabled: bool, host: str) -> MqttHelper:
    if enabled:
        return RealMqttHelper(host)
    else:
        return FakeMqttHelper()
