from utils.configLoader import ConfigLoader


class Creator:
    "The Factory Class"
    @staticmethod
    def create_object(some_property):
        "A static method to get a concrete product"
        if some_property == 'a':
            return ConfigLoader()
        return None