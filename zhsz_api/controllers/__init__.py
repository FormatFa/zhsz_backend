from flask import Blueprint
from settings import Config

db=Config.db

api_blue = Blueprint('api', __name__, url_prefix='/api')
from . import auth
from . import data
from . import logonav
from .import sql