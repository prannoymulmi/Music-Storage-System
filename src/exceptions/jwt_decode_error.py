class JWTDecodeError(Exception):
    """ Exception raised when the jwt token cannot be issued or verified.

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message: str = "JWT decode error") -> None:
        self.message = message
        super().__init__(self.message)

