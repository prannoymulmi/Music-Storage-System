class WeakPasswordError(Exception):
    """ Exception raised when password is non-compliant to policies.

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message: str = "password is non-compliant") -> None:
        self.message = message
        super().__init__(self.message)

