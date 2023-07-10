import hashlib

import requests
from password_strength import PasswordPolicy
from pydantic.fields import defaultdict


HAVE_I_BEEN_PAWNED_URL = "https://api.pwnedpasswords.com/range/{}"

class PasswordUtil:
    @staticmethod
    def is_password_compromised_password_in_have_i_been_pawned(passwd: str) -> bool:
        sha1 = hashlib.sha1()
        sha1.update(passwd.encode())
        hex_digest = sha1.hexdigest().upper()
        # get the first five SHA1 hex
        hex_digest_f5 = hex_digest[:5]
        # The remaining hex
        hex_digest_remaining = hex_digest[5:]
        r = requests.get(HAVE_I_BEEN_PAWNED_URL.format(hex_digest_f5))
        leaked_passwd_freq = defaultdict(int)
        for passwd_freq in r.content.splitlines():
            pass_parts = passwd_freq.split(b":")
            passwd = pass_parts[0].decode()
            freq = pass_parts[1]
            leaked_passwd_freq[passwd] = int(freq)
        return hex_digest_remaining in leaked_passwd_freq

    @staticmethod
    def is_password_policy_non_compliant(passwd: str):
        policy = PasswordPolicy.from_names(
            length=8,  # min length: 2
            uppercase=2,  # need min. 2 uppercase letters
            numbers=2,  # need min. 2 digits
            special=2,  # need min. 2 special characters
            nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
        )
        strength_compliant: bool = policy.password(passwd).test()
        return strength_compliant