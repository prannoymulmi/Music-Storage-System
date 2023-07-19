from utils.configLoader import ConfigLoader
from .abstract_factory import AbstractFactory

"""
The concrete implementation of the abstract factory to create config loader.
"""
class ConfigFactory(AbstractFactory):

    def create_object(self, some_property):
        "A static method to get a concrete product"
        if some_property == 'config_loader':
            return ConfigLoader()
        return None