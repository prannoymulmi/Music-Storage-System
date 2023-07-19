class VirusFoundError(Exception):
    """ Exception raised when Virus is found.

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message: str = "Virus found cannot upload") -> None:
        self.message = message
        super().__init__(self.message)
