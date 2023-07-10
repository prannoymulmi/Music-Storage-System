import hashlib
class MusicUtils(object):
    _instance = None

    '''
    Making the class singleton so the constructor throws an error when the object is instantiated 
    '''
    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance

    @staticmethod
    def get_file_from_path(path) -> bytes:
        with open(path, 'rb') as file:
            binary_data = file.read()
        return binary_data

    @staticmethod
    def calculate_check_sum(data):
        return hashlib.sha256(data).hexdigest()