import hashlib
import re

import requests
from pydantic.fields import defaultdict

HAVE_I_BEEN_PAWNED_URL = "https://api.pwnedpasswords.com/range/{}"


class PasswordUtil(object):
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
    def is_password_compromised_password_in_have_i_been_pawned(passwd: str) -> bool:
        # The API requires the password to be hashed in SHA1.
        """
        Bandit false positive, as only the last 5 characters of the hash is tranamistted
        to have I been pawned at it requires SHA1.
        """
        sha1 = hashlib.sha1() # nosec
        sha1.update(passwd.encode())
        hex_digest = sha1.hexdigest().upper()
        """
        Source:
         <a href=https://sanatinia.medium.com/securely-check-if-a-password-is-compromised-in-python-be74bf52b0cc>    
         Only the get the last five chars of the hash as per documentation  https://haveibeenpwned.com/API/v2
        """
        #
        #
        hex_digest_f5 = hex_digest[:5]
        # The remaining hex
        hex_digest_remaining = hex_digest[5:]
        # Adding time out of 5 seconds to add as a circuit breaker
        r = requests.get(HAVE_I_BEEN_PAWNED_URL.format(hex_digest_f5), timeout=5)
        leaked_passwd_freq = defaultdict(int)
        for passwd_freq in r.content.splitlines():
            pass_parts = passwd_freq.split(b":")
            passwd = pass_parts[0].decode()
            freq = pass_parts[1]
            leaked_passwd_freq[passwd] = int(freq)
        return hex_digest_remaining in leaked_passwd_freq

    @staticmethod
    def is_password_policy_non_compliant(passwd: str):
        # regex cheat sheet <a href=https://www.rexegg.com/regex-quickstart.html>
        """
        (?=.*[A-Z].*[A-Z]) ensures there are at least two uppercase letters.
        (?=.*[a-z].*[a-z]) ensures there are at least two lowercase letters.
        (?=.*\\d.*\\d) ensures there are at least two digits.
        (?=.*[-+_!@#$%^&*.,?].*[-+_!@#$%^&*.,?]) ensures there are at least two special characters (-+_!@#$%^&*.,?).
        .{8,} matches any character (except newline) at least 8 times.
        """

        pattern = r"^(?=.*[A-Z].*[A-Z])(?=.*[a-z].*[a-z])(?=.*\d.*\d)(?=.*[-+_!@#%^&*.,?].*[-+_!@#%^&*.,?]).{8,50}$"
        matches = re.match(pattern, passwd)
        return matches is None
