import hashlib
import os

from exceptions.data_not_found import DataNotFoundError


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
        if not path:
            raise DataNotFoundError(f'Error: Path: {path} not found')
        try:
            with open(path, 'rb') as file:
                binary_data = file.read()
            return binary_data
        except Exception:
            raise DataNotFoundError(f'{path} not found')

    @staticmethod
    def calculate_check_sum(data):
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def get_file_name_from_path(path):
        if path:
            return os.path.basename(path)
        return ""