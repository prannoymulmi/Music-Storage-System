import os

from pythonfuzz.main import PythonFuzz

"""
A python fuzz program to test the adding of new users. It uses python fuzz to generate random bytes in an infinite loop.
The random bytes are then converted into utf-8 to be fed into our add new user command.
"""


@PythonFuzz
def fuzz(buf):
    try:
        password = buf.decode("utf-8")
        if len(password) >= 5:
            result = os.system(
                f'python src/main.py add-new-user-and-role --username-admin "admin" --password-admin "#TWuJJ&BbMWbAnS*5r1J" '
                f'--new-username tester_3 --new-user-password "{password}" --role NORMAL_USER')
            # Stop the loop if the command succeeds
            if result == 1:
                raise Exception
    # Some bytes cannot be decoded, so we skip those values to keep the test running
    except UnicodeDecodeError:
        pass
    except ValueError:
        pass


if __name__ == '__main__':
    fuzz()
