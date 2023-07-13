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

The cyclomatic complexity of the code can be tested using the following commands

``` bash
radon cc -a src 
```


## Using Password Strength to set password policy
This gives an easy method to set password policies for python projects (Password-strength. PyPI. (n.d.)). 
Also, the entropy for the  password policies can be set easily to achieve a stronger password.

``` python
from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=2,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)
policy.test('12345!')
```

### Types of roles in the Project
| Role id | Role Name   | Description                                              |
|---------|-------------|----------------------------------------------------------|
| 1       | ADMIN       | Is allowed to do all the actions                         |
| 2       | NORMAL_USER | Is only allowed to view/change items created by the user |

### Commands for the applicaiton
``` bash
# Add-new-role
python src/main.py add-new-user-and-role --username-admin <CHANGE_USER> --password-admin <CHANGE_PASSWORD> --new-username <CHANGE_USER>--new-user-password <CHANGE_PASSWORD> --role NORMAL_USER

# Login
python src/main.py login --username <CHANGE_USER> --password <CHANGE_PASSWORD> 

# Add Music Data
python src/main.py add-music-data --username <CHANGE_USER> --password <CHANGE_PASSWORD>  --music-file-path audio_file_test.mp3 --music-score 1 --lyrics-file-path test.txt  

# list with token
 python src/main.py list-music-data  

 #list without token
 python src/main.py list-music-data --username <CHANGE_USER> --password <CHANGE_PASSWORD>


# Update music data
python src/main.py update-music-data --username <CHANGE_USER> --password <CHANGE_PASSWORD> --music-file-path audio_file_test.mp3 --music-data-id 8
```

### Run tests with coverage

```bash
coverage run --source=src -m pytest -v tests && coverage report -m 

# Generate result in 
coverage html && open htmlcov/index.html  
```

### Data Integrity
The project handles with the upload of various music data such as audio files 
and lyric file which has to ensure that no tampering within the database is 
carried out. A checksum is calculated using SHA-256 (Rachmawati, D et.al, 2018)
to ensure that the data inside the database are not tampered.

### Encryption
The sensitive data such as user_name, music_data are encrypted using SHA-512

### References
* Jones, M., Bradley, J. and Sakimura, N., 2015. Json web token (jwt) (No. rfc7519).
* Password-strength. PyPI. (n.d.). https://pypi.org/project/password-strength/ 
* Rachmawati, D., Tarigan, J.T. and Ginting, A.B.C., 2018, March. A comparative study of Message Digest 5 (MD5) and SHA256 algorithm. In Journal of Physics: Conference Series (Vol. 978, p. 012116). IOP Publishing.
