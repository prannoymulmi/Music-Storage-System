from abc import ABC, abstractmethod
"""
Following Abstract Factory Pattern
Allows decoupling of instances, as the instances are created from another source, helps in mocking dependencies while testing
"""


class AbstractFactory(ABC):
    """
    Abstract method which has to be implemented
    """

    @abstractmethod
    def create_object(self):
        pass
