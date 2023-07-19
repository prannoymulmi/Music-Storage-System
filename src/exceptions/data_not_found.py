class DataNotFoundError(Exception):
    """ Exception raised when the data in the database is nor found or file not found

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message: str = "data is not found") -> None:
        self.message = message
        super().__init__(self.message)

