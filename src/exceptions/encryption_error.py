class EncryptionError(Exception):
    """ Exception raised when the data cannot be encrypted or decrypted
    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

