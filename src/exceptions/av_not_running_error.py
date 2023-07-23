class AVNotRunningError(Exception):
    """ Exception raised when the antivirus file is not running

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message: str = "data is not found") -> None:
        self.message = message
        super().__init__(self.message)
