from flask_cors import CORS
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_openid import OpenID

csrfp=CSRFProtect()
cors=CORS()
lm=LoginManager()
bcrypt=Bcrypt()
oid=OpenID()