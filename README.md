# Description

# Getting Started 🚀

### Prerequisites for running the Notebooks for the simulations
* <a href=https://www.python.org/downloads/release/python-370/> Python 3.7 or Greater</a>
* <a href=https://pip.pypa.io/en/stable/installation/> pip 21.3.1 or Greater</a>

After installing the requirements, run the following commands in order
```bash
# creates python virtual environment for the project
python -m venv ./venv 

# activates virtual environment; this is on Mac or Linux
source ./venv/bin/activate 

# This is for windows (Using Powershell)
.\venv\Scripts\activate.bat 

# upgrade pip to get the latest packages
python -m pip install --upgrade pip 

#Is used to check if the virtual environment is being used 
pip -V  

# Install all required dependencies
pip install -r requirements.txt 
```

### JWT Tokens
The Jwt token store user claims like user id, expiry date, permissions (Jones, M., Bradley, J. and Sakimura, N., 2015).
This token is stored in a config when the users successfully logs-in. The token in this
application is only used for read actions, as this would give the user a better user experience 
by not making them log-in multiple times to read data. However, for sensitive actions such as delete, modify, and add a
re-authentication is required and the token is not used.

```
class Token(BaseModel):
    iss: str
    sub: str
    iat: int
    exp: int
    user_id: str
    permission: [str]
```

### Cyclomatic Complexity 

test using 

``` bash
radon cc -a src 
```


## Using Password Strength to set password policy
This gives an easy method to set password policies for python projects (Password-strength. PyPI. (n.d.)). 
Also, the entropy for the  password policies can be set easily to achieve a stronger password.
```
from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=2,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)
policy.test('ABcd12!')
```
## References

Jones, M., Bradley, J. and Sakimura, N., 2015. Json web token (jwt) (No. rfc7519).
Password-strength. PyPI. (n.d.). https://pypi.org/project/password-strength/ 