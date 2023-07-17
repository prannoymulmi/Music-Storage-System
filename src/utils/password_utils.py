import hashlib
import re

import requests
from pydantic.fields import defaultdict

HAVE_I_BEEN_PAWNED_URL = "https://api.pwnedpasswords.com/range/{}"

class PasswordUtil:
    @staticmethod
    def is_password_compromised_password_in_have_i_been_pawned(passwd: str) -> bool:
        sha1 = hashlib.sha1()
        sha1.update(passwd.encode())
        hex_digest = sha1.hexdigest().upper()
        # get the first five SHA1 hex
        # Only the get the last five chars of the hash as per documentation  https://haveibeenpwned.com/API/v2
        hex_digest_f5 = hex_digest[:5]
        # The remaining hex
        hex_digest_remaining = hex_digest[5:]
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
        # <a href=https://uibakery.io/regex-library/password-regex-python> strong password regex
        # password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[\[\]<>#?!@$%^&*-]).{8,30}$"
        pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[\[\]<>#?!@$%^&*-]).{8,30}$"
        matches = re.match(pattern, passwd)
        return matches is None
