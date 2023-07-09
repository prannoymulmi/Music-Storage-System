class UserNotFound(Exception):
    """ Exception raised when the user is not found

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message: str = "access_denied") -> None:
        self.message = message
        super().__init__(self.message)

