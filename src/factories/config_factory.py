from .abstract_factory import AbstractFactory
from utils.configLoader import ConfigLoader


class ConfigFactory(AbstractFactory):
    "The Factory Class"

    def create_object(self, some_property):
        "A static method to get a concrete product"
        if some_property == 'config_loader':
            return ConfigLoader()
        return None