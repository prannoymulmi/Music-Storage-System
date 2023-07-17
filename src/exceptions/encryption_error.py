class EncryptionError(Exception):
    """ Exception raised when the user is not authenticated or authorized.

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

