from abstract_factory import AbstractFactory
from utils.configLoader import ConfigLoader


class ConfigFactory(AbstractFactory):
    "The Factory Class"
    @staticmethod
    def create_object(some_property):
        "A static method to get a concrete product"
        if some_property == 'config_loader':
            return ConfigLoader()
        return None