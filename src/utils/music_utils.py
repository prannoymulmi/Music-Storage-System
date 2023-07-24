import hashlib
import os

from pyclamd import pyclamd
from rich import print

from exceptions.av_not_running_error import AVNotRunningError
from exceptions.data_not_found import DataNotFoundError
from exceptions.virus_found import VirusFoundError


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

    """
    Method which calculates the SHA256
    """

    @staticmethod
    def calculate_check_sum(data):
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def get_file_name_from_path(path):
        if path:
            return os.path.basename(path)
        return ""

    @staticmethod
    def write_bytes_to_file(bytes_to_write: bytes, path: str):
        try:
            with open(path, 'wb') as file:
                file.write(bytes_to_write)
        except Exception:
            raise DataNotFoundError(f'{path} not found')

    """
    Method which scans a file for viruses. 
    The bytes for the files are read and the fed into the function which then determines using its database if a virus is present or not.
    source <a href=https://xael.org/pages/pyclamd-en.html />
    """

    @staticmethod
    def scan_file(path):
        try:
            # Connect to ClamAV daemon
            cd = pyclamd.ClamdAgnostic()

            # Check if ClamAV daemon is running
            if not cd.ping():
                print("ClamAV daemon is not running.")
                return

            with open(path, 'rb') as f:
                file_bytes = f.read()

            # Scan the file bytes for viruses
            result = cd.scan_stream(file_bytes)

            # Check the scan result
            if result is None:
                print(f"[bold green] For path: {path}, No virus found [bold green]")
            else:
                raise VirusFoundError(f"{path}: virus found")
        except ValueError:
            raise AVNotRunningError("ClamAV is not running cannot upload file")
